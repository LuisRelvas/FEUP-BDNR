<?php
require '../vendor/autoload.php'; // Composer autoloader for MongoDB PHP library

// MongoDB connection
function getMongoDBConnection() {
    try {
        $client = new MongoDB\Client("mongodb://localhost:27017");
        return $client->miniforum->topics; // database->collection
    } catch (Exception $e) {
        die("Error connecting to MongoDB: " . $e->getMessage());
    }
}
?>