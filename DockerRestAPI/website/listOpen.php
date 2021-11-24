<html>
    <head>
        <title>CIS 322 REST-api demo: Laptop list</title>
    </head>
    <body>
        <h1>List of Open Brevets</h1>
        <ul>
        <?php
            $json = file_get_contents('http://laptop-service/listOpenOnlyAPI');
            $obj = json_decode($json);
	          $laptops = $obj->Brevets;
            //   var_dump($laptops);
            foreach ($laptops as $l) {
                // var_dump($laptops);
                echo "<li>$l</li>";
            }
            ?>
        </ul>
    </body>
</html>
