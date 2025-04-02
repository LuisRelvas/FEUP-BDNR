<?php

# ROUTE HANDLER
$request_uri = $_SERVER['REQUEST_URI'];
$url = parse_url($request_uri, PHP_URL_PATH);

if ($url == '/' || $url == '/index.php') {
} 

elseif (preg_match('/^\/listings\/(\d+)$/', $url, $matches)) {
    $listing_id = $matches[1];
    include 'listingPage.php';
    exit;
} 
elseif (preg_match('/^\/hosts\/(\d+)$/', $url, $matches)) {
    $host_id = $matches[1];
    include 'hostPage.php';
    exit;
} 
else {
    header("HTTP/1.0 404 Not Found");
    echo "<h1>404 Not Found</h1>";
    echo "<p>The page you requested could not be found.</p>";
    exit;
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Listings</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
    </style>
</head>
<body>
    <h1>Listings</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Picture</th>
                <th>Name</th>
                <th>Price</th>
                <th>Host</th>
                <th>Location</th>
                <th>Rating</th>

            </tr>
        </thead>
        <tbody>
            <?php
            $urlListings = 'http://localhost:5000/listings'; // URL da API
            $json = file_get_contents($urlListings);
            $listings = json_decode($json, true);

            $urlHosts = 'http://localhost:5000/hosts'; // URL da API
            $jsonHosts = file_get_contents($urlHosts);
            $hosts = json_decode($jsonHosts, true);

            if ($listings) {
                foreach ($listings as $listing) {
                    echo "<tr>
                            <td>{$listing['listing_id']}</td>
                            <td><a href='{$listing['picture_url']}' target='_blank'>Link</a></td>
                            <td><a href='/listings/{$listing['listing_id']}'>{$listing['name']}</a></td>
                            <td>" . number_format($listing['price'], 2) . "</td>
                            <td><a href='/hosts/{$listing['host_id']}'>{$listing['host_id']}</a></td>
                            <td>{$listing['neighbourhood_cleansed']}</td>
                            <td>{$listing['rating']}</td>
                          </tr>";
                }
            } else {
                echo "<tr><td colspan='7'>Nenhum dado encontrado.</td></tr>";
            }
            ?>
        </tbody>
    </table>
    <h1>Hosts</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Host Location</th>
                <th>About</th>
                <th>Response Time</th>
                <th>Picture</th>
            </tr>
        </thead>
        <tbody>
            <?php
            if ($hosts) {
                foreach ($hosts as $host) {
                    echo "<tr>
                            <td>{$host['host_id']}</td>
                            <td>{$host['host_name']}</td>
                            <td>{$host['host_location']}</td>
                            <td>{$host['host_about']}</td>
                            <td>{$host['host_response_time']}</td>
                            <td>{$host['host_picture_url']}</td>
                          </tr>";
                }
            } else {
                echo "<tr><td colspan='7'>Nenhum dado encontrado.</td></tr>";
            }
            ?>
        </tbody>
</body>
</html>
