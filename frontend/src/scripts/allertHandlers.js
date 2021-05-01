import swal from 'sweetalert'

export function raiseError(text){
    swal({
        title: "Fail!",
        text: text,
        icon: "error",
    })
}

export function raiseAllertDelete(text){
    return swal({
        title: "Warning!",
        icon: "warning",
        text: text,
        buttons: {
        no: {
            text: "No",
            value: false,
        },
        yes: {
            text: "Yes",
            value: true,
            className: "sweet-confirm",
        },
        },
    });
}

export function raiseSuccess(text){
    return swal({
        title: "Success!",
        text: text,
        icon: "success",
    })
}