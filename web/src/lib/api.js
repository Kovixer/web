import getToken from './token';


import { server } from '../sets';


async function serverRequest(json={}) {
    return fetch(server, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(json),
    })
    .catch((error) => {
        let errCode;
        const errText = error.toString();

        if (errText === 'Error: Request failed with status code 429') {
            errCode = 429;
        } else if (errText === 'Error: Network Error') {
            errCode = 'network';
        } else {
            errCode = 400;
        }

        return {
            error: errCode,
            data: errText,
        };
    });
}

export default function api(method, params={}) {
    return new Promise((resolve, reject) => {
        const json = {
            method,
            params,
            network: 'web',
            language: localStorage.getItem('locale'),
            token: getToken(),
        };

        serverRequest(json).then(async (responce) => {
            const res = await responce.json();

            if (res.error !== 0) {
                console.log(res.data);
                reject(res.error, res.data);
            } else if (res.data === undefined) {
                resolve({});
            } else {
                resolve(res.data);
            }
        });
    });
}

// TODO: Socket.IO
