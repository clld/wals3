WALS = {}

WALS.make_style_map = function (name) {
    var styles = new OpenLayers.StyleMap({
        "default": {
            pointRadius: 8,
            strokeColor: "black",
            strokeWidth: 1,
            fillColor: "${icon_color}",
            fillOpacity: 0.9,
            graphicXOffset: 50,
            graphicYOffset: 50,
            graphicZIndex: 20
        },
        "temporary": {
            pointRadius: 12,
            fillOpacity: 1,
            label : "${name}",
            fontColor: "black",
            fontSize: "12px",
            fontFamily: "Courier New, monospace",
            fontWeight: "bold",
            labelAlign: "cm",
            labelOutlineColor: "white",
            labelOutlineWidth: 3
        },
        "select": {
            label: "",
            pointRadius: 10
        }
    }),
        wals_icons = {
      "s": {graphicName: "square"}, // square
      "d": {graphicName: "square", rotation: 45}, // diamond
      "t": {graphicName: "triangle"},
      "f": {graphicName: "triangle", rotation: 180},
      "c": {graphicName: "circle"}
    };
    styles.addUniqueValueRules("default", "icon_type", wals_icons);
    styles.addUniqueValueRules("select", "icon_type", wals_icons);
    return styles;
}

CLLD.Map.style_maps["wals_feature"] = WALS.make_style_map("wals_feature");
