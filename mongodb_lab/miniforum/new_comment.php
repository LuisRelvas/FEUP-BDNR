<?php
require_once 'config.php';

// Check if form is submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Validate form data
    if (empty($_POST['topic']) || empty($_POST['comment']) || empty($_POST['author'])) {
        die("Error: All fields are required.");
    }
    
    $topicId = $_POST['topic'];
    $comment = $_POST['comment'];
    $author = $_POST['author'];
    
    // Add comment to the topic
    $collection = getMongoDBConnection();
    
    try {
        $result = $collection->updateOne(
            ['_id' => new MongoDB\BSON\ObjectId($topicId)],
            ['$push' => [
                'comments' => [
                    'text' => $comment,
                    'author' => $author
                ]
            ]]
        );
        
        // Redirect to index with topic parameter
        header("Location: index.php?topic=" . $topicId);
        exit;
    } catch (Exception $e) {
        die("Error adding comment: " . $e->getMessage());
    }
} else {
    // Not a POST request, redirect to index
    header("Location: index.php");
    exit;
}
?>