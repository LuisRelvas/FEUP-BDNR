<?php
require_once 'config.php';

// Check if form is submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Validate form data
    if (empty($_POST['title']) || empty($_POST['body']) || empty($_POST['author'])) {
        die("Error: All fields are required.");
    }
    
    $title = $_POST['title'];
    $body = $_POST['body'];
    $author = $_POST['author'];
    
    // Create new topic document
    $collection = getMongoDBConnection();
    
    try {
        $result = $collection->insertOne([
            'title' => $title,
            'body' => $body,
            'author' => $author,
            'comments' => []
        ]);
        
        // Redirect to index
        header("Location: index.php");
        exit;
    } catch (Exception $e) {
        die("Error inserting new topic: " . $e->getMessage());
    }
} else {
    // Not a POST request, redirect to the form
    header("Location: new_topic.html");
    exit;
}
?>