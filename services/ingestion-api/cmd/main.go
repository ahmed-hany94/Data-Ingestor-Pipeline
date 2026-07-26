package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
)

var REDIS_QUEUE_KEY = getEnv("REDIS_QUEUE_KEY", "data_queue")

type Payload struct {
	Name  string `json:"name" binding:"required"`
	Value string `json:"value" binding:"required"`
}

func getEnv(key, fallback string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return fallback
}

func main() {
	router := gin.Default()

	// connect to redis
	ctx := context.Background()
	rdb := redis.NewClient(&redis.Options{
		Addr:     getEnv("REDIS_URL", "localhost:6379"),
		Password: getEnv("REDIS_PASSWORD", ""),
		DB:       0,
	})
	defer rdb.Close()

	// if no connection, error and quit
	pong, err := rdb.Ping(ctx).Result()
	if err != nil {
		log.Fatalf("Could not connect to Redis: %v", err)
	}
	fmt.Printf("Successfully connected! Server responded with: %s\n", pong)

	router.GET("/healthz", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "Ok",
		})
	})

	// register an endpoint that receives some data for now
	// push to the redis queue using LPUSH
	router.POST("/data", func(c *gin.Context) {
		var payload Payload
		if err := c.ShouldBindJSON(&payload); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"success": false,
				"error":   err.Error(),
			})
			return
		}

		jsonData, err := json.Marshal(payload)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{
				"success": false,
				"error":   "Failed to process internal data payload",
			})
			return
		}

		_, err = rdb.LPush(ctx, REDIS_QUEUE_KEY, jsonData).Result()
		if err != nil {
			log.Printf("LPush failed: %v", err) // Logs error safely without knocking the server offline
			c.JSON(http.StatusInternalServerError, gin.H{
				"success": false,
				"error":   "Failed to write to queue",
			})
			return
		}

		c.JSON(http.StatusOK, gin.H{
			"success": true,
			"error":   "",
		})
	})

	router.Run()
}
