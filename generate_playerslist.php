<?php 

//Used to create the initial player-layout

$num_players=8;

echo('
<div id="players">');
for ($i=1; $i<$num_players+1; $i++){ 
    echo('
    <div id="p' . $i . '" class="block">
        <div id="p' . $i . '_rank">
        ' . $i . ':
        </div>
        <div id="p' . $i . '_name">
            <input type="text" placeholder="Spielername" name="name_p' . $i . '" id="name_p' . $i . '"
            onchange="PlayerNameChanged(name_p' . $i . ')" onmouseenter="PlayerOnHover(\'p' . $i . '\')" onmouseleave="PlayerOnNoHover(\'p' . $i . '\')" />
        </div>
        <div id="p' . $i . '_points">
            <input type="number" min="0" placeholder="Punkte" name="points_p' . $i . '" id="points_p' . $i . '" onchange="PlayerPointsChanged(\'points_p' . $i . '\')"/>
        </div>
    </div>'
    );
}
echo('
</div>');

echo('

########################
');

echo('
    var player_uis = [];');
for ($i=1; $i<$num_players+1; $i++){ 
    echo('
    player_uis.push({id: "p' . $i . '", rank: "p' . $i . '_rank", name: "p' . $i . '_name", textbox_name: "name_p' . $i . '", textbox_points: "points_p' . $i . '"});');
    }
    echo('

    ');
?>
