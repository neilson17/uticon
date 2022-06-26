function getDetail(url, name, desc, list_price, sale_price, brand, category, image){
    $('#productName').html(name);
    $('#productDescription').html(desc);
    if (image != "no"){
        $('.imgModal').attr('src', image);
        $('.hrefModal').attr('href', image);
    }
    else {
        var noimage = $('#no-image').val();
        $('.imgModal').attr('src', noimage);
        $('.hrefModal').attr('href', noimage);
    }
    var text = "";
    if (list_price != sale_price) {
        text += "<h5><s>$" + list_price + "</s></h5>";
    }
    text += "<h5>$" + sale_price + "</h5>";
    
    $('#productPrice').html(text);
    $('#productUrl').attr('href', url);
    $('#productBrand').html(brand);
    $('#productCategory').html(category);
}