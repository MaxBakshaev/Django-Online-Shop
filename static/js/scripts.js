function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i])

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}

const csrftoken = getCookie('csrftoken')

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
}

$.ajaxSetup({
    beforeSend: (xhr, settings) => {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})


const add_to_favorites_url = '/favorites/add_to_favorites/'
const remove_from_favorites_url = '/favorites/remove_from_favorites/'
const favorites_api_url = '/favorites/favorites_api/'
const added_to_favorites_class = '/added/'


function add_to_favorites() {
    $('.add-to-favorites').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault()

            const type = $(el).data('type')
            const id = $(el).data('id')

            
            if( $(e.target).hasClass(added_to_favorites_class) ) {

                $.ajax({
                    url: remove_from_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        type: type,
                        id: id,
                    },
                    success: (data) => {
                        $(el).removeClass(added_to_favorites_class)
                        // $('form[name="remove-from-favorites-' + id + '"]').css('display', 'none')

                        get_session_favorites_statistics()
                    }
                })
            } else {

                $.ajax({
                    url: add_to_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        type: type,
                        id: id,
                    },
                    success: (data) => {
                        $(el).addClass(added_to_favorites_class)
                        // $('form[name="remove-from-favorites-' + id + '"]').css('display', 'block')

                        get_session_favorites_statistics()
                    }
                })
            }
        })
    })
}


// function remove_from_favorites() {
//     $('form.remove-from-favorites').each((index, el) => {
//         $(el).find('button[type="submit"]').click((e) => {
//             e.preventDefault()

//             const page_url = $(el).attr('action')
//             const id = $(el).find('input[name="id"]').val()

//             $.ajax({
//                 url: page_url,
//                 type: 'POST',
//                 dataType: 'json',
//                 data: {
//                     'id': id,
//                 },
//                 success: (data) => {
//                     $(el).css('display', 'None')
//                     $('form[name="add-to-favorites-' + id + '"]').find('button.btn-success').prop('disabled', false)

//                     get_session_favorites_statistics()
//                 }
//             })
//         })
//     })
// }


function get_session_favorites() {
    get_session_favorites_statistics()

    $.getJSON(favorites_api_url, (json) => {
        if (json !== null) {
            for (let i = 0; i < json.length; i++) {

                // $('form.remove-from-favorites').each((index, el) => {
                //     const id = $(el).find('input[name="id"]').val()

                //     if ( json[i].id == id ) {
                //         $(el).css('display', 'block')
                //     }
                // })

                $('.add-to-favorites').each((index, el) => {
                    const id = $(el).data('id')

                    if ( json[i].type == type && json[i].id == id) {
                        $(el).addClass(added_to_favorites_class)
                    }
                })
            }
        }
    })
}


function get_session_favorites_statistics() {
    $.getJSON(favorites_api_url, (json) => {
        if (json !== null) {
            $('#favorites-statistics').empty()
            let sites_plural = json.length > 1 ? ' objects' : ' object'
            $('#favorites-statistics').html(json.length + sites_plural)
        }
        if (json == null) {
            $('#favorites-statistics').empty()
        }
    })
}


$(document).ready(function() {
    add_to_favorites()
    // remove_from_favorites()
    get_session_favorites()
})