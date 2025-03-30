<!DOCTYPE html>
<html>
<head>
    <title>Listing</title>
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
                <th>URL</th>
                <th>Name</th>
                <th>Description</th>
                <th>NeighborHood Overview</th>
                <th>Property Type</th>
                <th>Room Type</th>
                <th>Accommodates</th>
                <th>Bathrooms</th>
                <th>Bedrooms</th>
                <th>Amenities</th>
                <th>Host ID</th>
                <th>Host Name</th>
                <th>Minimum Nights</th>
                <th>Maximum Nights</th>
                <th>Price</th>
            </tr>
        </thead>
        <tbody>
            <?php
            $request_uri = $_SERVER['REQUEST_URI'];
            $url = parse_url($request_uri, PHP_URL_PATH);
            $url = explode('/', $url);
            $url[2] = isset($url[2]) ? $url[2] : 0;
            $urlListings = "http://localhost:5000/listings/{$url[2]}"; // URL da API
            $json = file_get_contents($urlListings);
            $listing = json_decode($json, true);

            if ($listing) {
                    echo "<tr>
                            <td>{$listing['id']}</td>
                            <td><a href='{$listing['listing_url']}' target='_blank'>Link</a></td>
                            <td>{$listing['name']}</td>
                            <td>{$listing['description']}</td>
                            <td>{$listing['neighborhood_overview']}</td>
                            <td>{$listing['property_type']}</td>
                            <td>{$listing['room_type']}</td>
                            <td>{$listing['accommodates']}</td>
                            <td>{$listing['bathrooms']}</td>
                            <td>{$listing['bedrooms']}</td>
                            <td>{$listing['amenities']}</td>
                            <td><a href='/hosts/{$listing['host_id']}'>{$listing['host_id']}</a></td>
                            <td>{$listing['host_name']}</td>
                            <td>{$listing['minimum_nights']}</td>
                            <td>{$listing['maximum_nights']}</td>
                            <td>" . number_format($listing['price'], 2) . "</td>
                          </tr>";
            } else {
                echo "<tr><td colspan='7'>Nenhum dado encontrado.</td></tr>";
            }
            ?>
        </tbody>
    </table>
</body>

</html>
