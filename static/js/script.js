amount_cart = 0
// Bộ lọc
$("#sort-select").change(function() {
    if ($(this).val() != null) {
        addField('sort', $(this).val())
    }
})

$("input[name=filter-price]").click(function() {
    if ($(this).attr("value") != null) {
        addField('filter', $(this).attr("value"))
    }
})

function addField(field, value) {
    href = window.location.href.replace(/\?.*/, '');
    var re = new RegExp('\/'+field+'\/[^\/$]*');
    if (href.search(re) != -1) {
        href = href.replace(re, "/"+field+"/"+value);
    }
    else {
        href = href + "/" + field + "/" + value;
    }
    window.location.href = href;
}

function deleteProductInCart(e, id) {
    // handle front-end
    e.closest('.clearfix.text-left').previousElementSibling.remove();
    e.closest('.clearfix.text-left').remove();
    


    // Ẩn nút đặt hàng khi thêm sản phẩm
    if (amount_cart == 1) {
        $('input[name=checkout]').attr("disabled", true);
    }
    else {
        $('input[name=checkout]').attr("disabled", false);
    }

    // handle back-end
    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });
    $.ajax({
        type: "post",
        url: "/site/ajax/deletecart",
        data: { MaSP: id },
        success: function(response) {
            amount_cart = response['amount'];
            $('.number-total-product').html(response['amount']);
            $('.price-total').html(number_format(response['totalAll']) + '₫');
        }
    });
}

function addProductInCart(id, amount = 1) {
    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });
    totalAll = 0;
    totalProduct = 0;
    $.ajax({
        type: "post",
        url: "/site/ajax/addcart",
        data: { MaSP: id, amount: amount},
        success: function(response) {
            
            $('input[name=checkout]').attr("disabled", false);
            // frontend
            count = $('.number-total-product').html();
            // Hiển thị nút đặt hàng khi thêm sản phẩm
            product_image = response['product_image'];
            totalProduct = response['totalProduct'];
            totalAll = response['totalAll'];
            amount_cart = response['amount'];
            if ("" != product_image) {
                $('.number-total-product').html(response['amount']);

                $('.cart-product').append('<hr><div class="clearfix text-left">\
                <div class="row">\
                    <div class="col-sm-6 col-md-1">\
                        <div><img class="img-responsive" src="/static' + product_image.image + '" alt="' + product_image.product.TenSP + '"></div>\
                    </div>\
                    <div class="col-sm-6 col-md-3"><a class="product-name" href="' + $('#route').val() + '?id=' + product_image.product.MaSP + '">' + product_image.product.TenSP + '</a></div>\
                    <div class="col-sm-6 col-md-2"><span class="product-item-discount">' + number_format(product_image.price_sale) + '₫</span></div>\
                    <div class="col-sm-6 col-md-3">\
                        <input type="number" onchange="updateProductInCart(this,'+"'"+product_image.product.MaSP+"')"+'" min="1" value="1">\
                    </div>\
                    <div class="col-sm-6 col-md-2 total' + product_image.product.MaSP + '"><span>' + number_format(product_image.price_sale) + '₫</span></div>\
                    <div class="col-sm-6 col-md-1"><a class="remove-product" href="javascript:void(0)" onclick="deleteProductInCart(this,' + "'" + product_image.product.MaSP + "'" + ')">\
                        <span class="glyphicon glyphicon-trash"></span></a></div>\
                </div>\
            </div>');
            }
            $('.total' + id).html(number_format(totalProduct) + '₫');
            $('.price-total').html(number_format(totalAll) + '₫');
        }
    });
}

function addComment(comment) {
    more = $("#more");
    r = $("<input>");
    r.addClass("answered-rating-input");
    r.attr({"name": "rating", type: "text", "value": comment.rate, "readonly": "readonly"});
    $('<hr><span class="date pull-right">'+comment.ThoiGian+'</span>').insertBefore(more);
    r.insertBefore(more)
    $('<span class="by">'+comment.TenKH+'</span><p>'+comment.ChiTiet+'</p>').insertBefore(more);
    r.rating({
        min: 0,
        max: 5,
        step: 1,
        size: 'md',
        stars: "5",
        showClear: false,
        showCaption: false
    });
}

function clear(name, string) {
    $('select[name=' + name + ']').empty();
    $('select[name=' + name + ']').append('<option value="0">' + string + '</option>');
}

function add(name, list) {
    list.forEach(element => {
        // console.log(element)
        $('select[name=' + name + ']').append('<option value="' + element[0] + '">' + element[1] + '</option>');
    });
}

var countcomment = 1;
var countproduct = [];
const amountcomment = 5;
const amountproduct = 4;
var checkEmail = false;
var checkoldpass = false;
var over = false
function updateProductInCart(el, id) {
    amount = el.value;
    // console.log(id + ':' + amount);
    // backend
    addProductInCart(id, amount);
}

$(document).ready(function() {

    // So khớp mật khẩu
    $('input[name=old_password]').keyup(function() {
        password = $(this).val();
        username = $('input[name=username]').val();
        $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            }
        });
        $.ajax({
            type: "POST",
            url: "/site/ajax/checkpassword",
            data: {username: username, password: password},
            success: function(response) {
                if (!response['result_check_pass']) {
                    $('.enter_old_pass').css('color', 'red')
                    $('.enter_old_pass').text('Mật khẩu không khớp!')
                    $('#editinfo').attr('disabled', 'disabled');
                }
                else {
                    $('.enter_old_pass').css('color', 'green')
                    $('.enter_old_pass').text('Khớp mật khẩu!')
                    $('#editinfo').removeAttr('disabled');
                }
            }
        });
    });

    // addCart
    $('input[name=checkout]').click(function() {
        window.location.href = $(this).attr('urls');
    });

    $('.addCart').click(function() {
        id = $(this).attr('product-id');
        addProductInCart(id);
    });

    // Email exist
    $('#email').change(function() {
        $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            }
        });
        $.ajax({
            type: "get",
            url: "/account/check",
            data: { email: $('#email').val() },
            success: function(response) {
                checkEmail = response == 1 ? false : true;
                if (response == 1) {
                    $('#describe-email').html('Email đã tồn tại!').css('color', 'red');
                } else {
                    $('#describe-email').html('Bạn có thể đăng kí với email này!').css('color', 'green');
                }
            }
        });
    });
    
    // Password
    $('input[name=re-password]').keyup(function() {
        if ($(this).val() == $('input[name=password]').val() && checkEmail) {
            $('#sign-up').removeAttr('disabled');
        }
    });
    // Search 
    // $('.js-example-basic-multiple').select2();
    $('.js-example-basic-multiple').change(function() {
        // console.log(1);
        // console.log(keyword);
    });

    // Ajax district list
    $('select[name=province]').click(function() {
        id = $('select[name=province]').val();
        clear('district', 'Quận / Huyện');
        clear('ward', 'Phường / Xã');
        if (id != null) {
            $.ajaxSetup({
                headers: {
                    'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
                }
            });
            $.ajax({
                type: "POST",
                url: "/site/ajax/districts",
                data: { province: id },
                success: function(response) {
                    if (response != null) {
                        districts = response.districts
                        price = response['price']
                        if ($('.shipping-fee')) {
                            $('.shipping-fee').html(number_format(price) + '₫');
                            total = $('.payment-total');
                            if (total.length != 0) {
                                total.html(number_format(price + response['totalAll']) + '₫');
                            }
                        }
                        add('district', districts);
                    }
                }
            });
        }
    });

    // Ajax wards list
    $('select[name=district]').change(function() {
        id = $('select[name=district]').val();
        clear('ward', 'Phường / Xã');
        if (id != null) {
            $.ajaxSetup({
                headers: {
                    'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
                }
            });
            $.ajax({
                type: "POST",
                url: "/site/ajax/wards",
                data: { district: id },
                success: function(response) {
                    if (response != null) {
                        wards = response.wards;
                        add('ward', wards);
                    }
                }
            });
        }
    });

    $('input[name=search').blur(function() {
        if (!over) {
            $('.search-result').hide();
        }
    });

    $('input[name=search').focus(function() {

        $('.search-result').show();
    });

    $('.search-result').mouseenter(function() {
        over = true
    })

    $('.search-result').mouseleave(function() {
        over = false
    })

    $('#input-3').rating({ displayOnly: true, step: 0.5 });
    $("#sort-select").val($('#sortSelected').val());
    $("#filter-" + $('#PriceRange').val()).attr('checked', 'checked');

    // Xem thêm bình luận
    $('#more-comment').click(function() {
        $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            }
        });
        $.ajax({
            type: "POST",
            url: "/site/myaccount/morecomment",
            data: {id_product: $('input[name=MaSP]').val(), current_comment: $('input[name=current_comment]').val()},
            success: function(response) {
                // console.log(response.still);
                comments = response['comments'];
                current_comment = response.current_comment;
                // alert(current_comment)
                still = response.still;
                comments.forEach(comment => {
                    addComment(comment);
                });
                $('input[name=current_comment').val(response.current_comment);
                if (!response.still) {
                    $('#more').empty().append('<p>Đã xem hết bình luận của sản phẩm này!</p>');
                }
            }
        });
    });



    // Hiện lên "Xem chi tiết" và "Thêm vào giỏ hàng" khi hover vào sản phẩm
    $(".product-container").hover(function() {
        $(this).children(".button-product-action").toggle(400);
    });

    // Khi click vào button back to top, sẽ cuộn lên đầu trang web trong vòng 0.8s
    $(".back-to-top").click(function() {
        $("html").animate({ scrollTop: 0 }, 800);
    });

    // Hiển thị cart dialog
    $('.btn-cart-detail').click(function() {
        $('#modal-cart-detail').modal('show');
    });

    // Cập nhật hình chính khi click vào thumbnail hình ở slider
    $('main .product-detail .product-detail-carousel-slider img').click(function(event) {
        /* Act on the event */
        $('main .product-detail .main-image-thumbnail').attr("src", $(this).attr("src"));
        var image_path = $('main .product-detail .main-image-thumbnail').attr("src");
        $(".zoomWindow").css("background-image", "url('" + image_path + "')");

    });


    $('.rating-input').rating({
        min: 0,
        max: 5,
        step: 1,
        size: 'md',
        stars: "5",
        showClear: false,
        showCaption: false
    });

    $('main .product-detail .product-description .answered-rating-input').rating({
        min: 0,
        max: 5,
        step: 1,
        size: 'md',
        stars: "5",
        showClear: false,
        showCaption: false,
        displayOnly: false,
        hoverEnabled: true
    });

    $('main .ship-checkout[name=payment_method]').click(function(event) {
        /* Act on the event */
    });

    $('input[name=back-shopping]').click(function(event) {
        /* Act on the event */
        $('#modal-cart-detail').modal('hide');
    });

    // Hiển thị carousel for relative products
    $('main .product-detail .product-related .owl-carousel').owlCarousel({
        loop: true,
        margin: 10,
        nav: true,
        dots: false,
        responsive: {
            0: {
                items: 2
            },
            600: {
                items: 4
            },
            1000: {
                items: 5
            }
        }

    });
});

// Login in google
function onSignIn(googleUser) {
    var id_token = googleUser.getAuthResponse().id_token;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://study.com/register/google/backend/process.php');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        // console.log('Signed in as: ' + xhr.responseText);
    };
    xhr.send('idtoken=' + id_token);
}
function openMenuMobile() {
    $(".menu-mb").width("250px");
    $(".btn-menu-mb").hide("slow");
}

function closeMenuMobile() {
    $(".menu-mb").width(0);
    $(".btn-menu-mb").show("slow");
}