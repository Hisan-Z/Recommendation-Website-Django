$(function () {
    var sliderValues = [0,300, 500, 700, 1000, 1500, 10000000];

    $("#slider-range").slider({
        range: true,
        min: 0,
        max: sliderValues.length-1,
        values: [0, 5],
        slide: function (event, ui) {
            $("#amount").val("$" + sliderValues[ui.values[0]] + " - $" + sliderValues[ui.values[1]]);
            $("#minPriceInput").val(sliderValues[ui.values[0]]);
            $("#maxPriceInput").val(sliderValues[ui.values[1]]);
        },
        minDistance: 1,
        change: function (event, ui) {
            $("#myform").submit(); // Submit the form when the slider value changes
        }
    });

    $("#amount").val("$" + sliderValues[$("#slider-range").slider("values", 0)] + " - $" + sliderValues[$("#slider-range").slider("values", 1)]);
    $("#minPriceInput").val(sliderValues[$("#slider-range").slider("values", 0)]);
    $("#maxPriceInput").val(sliderValues[$("#slider-range").slider("values", 1)]);
});