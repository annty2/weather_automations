(() => {
    // const elements = [...document.querySelectorAll(`.zebra tbody tr`)];
    //
    // const city_temp_json = [];
    // for (const element of elements){
    //     const cities = element.querySelectorAll('a');
    //     const temps = element.querySelectorAll('.rbi');
    //
    //     for (let i = 0; i < 4; i++) {
    //         // if(!cities[i] || !temps[i]) {
    //         //     console.log(element);
    //         //     continue;
    //         // }
    //
    //         city_temp_json.push({
    //             city: cities[i].innerText, temp: temps[i].innerText,
    //         })
    //     }
    // }
    //
    // return JSON.stringify(city_temp_json);

    const city_temp = [...document.querySelectorAll(`.zebra td`)].filter(elem => elem.querySelector(`a`) || elem.className == "rbi").map(elem => elem.innerText.replace(`°C`, ``).replace(`*`, ``).trim());

    for (let i = 0, k = 0; i < city_temp.length; i = i + 2, k++) {
        city_temp_json[k] = {
            city: city_temp[i],
            temperature: city_temp[i + 1]
        };
    }

    return JSON.stringify(city_temp_json);
})();
