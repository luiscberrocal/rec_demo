/* Project specific Javascript goes here. */

(function ($) {

    $.fn.addRealEstateSpaces = function (url, options) {
        const card = $(this);
        // This is the easiest way to have default options.
        let settings = $.extend({
            // These are the defaults.
            color: "#556b2f",
            backgroundColor: "white"
        }, options);
        $.ajax({
            method: 'GET',
            url: url,
            data: {},
            success: function (data) {
                let tbody = card.find('tbody')
                console.log(tbody);
                let sum = 0.0
                data.real_estate_spaces.forEach(function (item) {
                    //console.log(item);
                    let row = tbody.append($('<tr>'));
                    row.append($('<td>').text(item.name));
                    row.append($('<td>').text(item.space_type))
                    row.append($('<td>').text(item.area))
                    let price = parseFloat(item.price).toLocaleString('en', {
                        useGrouping: true,
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    })
                    sum += parseFloat(item.price);
                    row.append($('<td>').text(price).addClass('price').attr('price', item.price))
                })
                let row = tbody.append($('<tr>'));
                row.append($('<td colspan="3">').text('Total'));
                let sumDisplay = parseFloat(sum).toLocaleString('en', {
                    useGrouping: true,
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                })
                row.append($('<td>').text(sumDisplay).addClass('price').attr('price', sum))

            }
        });

    };

}(jQuery));