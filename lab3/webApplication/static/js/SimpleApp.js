const requestURL = 'http://localhost:8000/calculation'

sendRequest = (number, callback) => {
    const xhr = new XMLHttpRequest()

    // xhr.responseType(JSON)
    xhr.open('POST', requestURL)

    xhr.onload = () => {
         console.log(xhr.response);
        const responseBody = JSON.parse(xhr.response);
        if (!responseBody) {
            return;
        }
        if (!callback) {
            return;
        }

        if (typeof responseBody.output_value !== 'undefined') {
            callback(responseBody.output_value);
        }
     }
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({input_value: number}))
}

showResult = (result) => {
    document.getElementById("output").value = result;
}

calculate = () => {
    const input = document.getElementById("input").value;
    if (input.length === 0) {
        alert('Given value is empty');
        return;
    }

    const number = Number(input);
    if (!Number.isInteger(number)) {
        alert('Given value is invalid: ' + input);
        return;
    }
    sendRequest(number, showResult);
}

