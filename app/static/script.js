const update_input = document.getElementById('update_input')

const delete_post = async () => {
    const response = await fetch(location.pathname, {
        method: 'DELETE'
    })

    if (response.ok) {
        window.location.href = '/'
    }
}


const update_post = async () => {
    const content = update_input.value

    const response = await fetch(location.pathname, {
        method: 'PUT',
        body: JSON.stringify({
            content
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })

    if (response.ok)
        window.location.href = location.pathname

}

