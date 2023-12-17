import puppeteer from 'puppeteer';


function delay(time : number) {
    return new Promise(resolve => setTimeout(resolve, time));
}


const CALENDAR_URL = "view-source:https://www.springtrainingconnection.com/schedule/cactus.html";

export async function scrapeDates() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    await page.setViewport({width: 1080, height: 1024});

    await page
        .goto(CALENDAR_URL, {
            waitUntil: "networkidle0",
        })
        .catch((err: Error) => console.log("error loading url", err));

    page.close();
}

/*
async function scrape_fords(zip) {

    const XLT = "https://shop.ford.com/inventory/maverick/results?zipcode=$ZIP$&Radius=50&modeltrim=Maverick_F26-XLT&SpecialPackage=XLT_Luxury_Package&ExteriorColor=B3%3BKU%3BEA&Engine=2_5l_hybrid&Drive=FWD&Order=LowPrice&displayStyle=list"
    const XLT_LARIAT = "https://shop.ford.com/inventory/maverick/results?zipcode=$ZIP$&Radius=50&modeltrim=Maverick_F26-XLT%3BMaverick_F26-LARIAT&SpecialPackage=XLT_Luxury_Package%3BLARIAT_Luxury_Package&ExteriorColor=B3%3BKU%3BEA&Engine=2_5l_hybrid&Drive=FWD&Order=LowPrice&displayStyle=list"

    const url = XLT_LARIAT.replace("$ZIP$", zip.zip_code)

    console.log(`Scraping: ${zip.city} (${zip.zip_code})...`)

    const page = await browser.newPage();

    await page.setViewport({width: 1080, height: 1024});

    await page
        .goto(url, {
            waitUntil: "networkidle0",
        })
        .catch((err) => console.log("error loading url", err));

    const _records = await page.evaluate(() => {

        const nodes = document.querySelectorAll('.exact-matches-container .card-list-view-top');
        const __records = [];

        const _priceToNumber = (price) => {
            return parseFloat(price.replace(/,/g, ''));
        }

        nodes.forEach((node, index) => {
            __records.push({
                index,
                name: node.querySelector('[data-bo-bind="vm.modelDisplayName"]').innerText,
                price: _priceToNumber(node.querySelector('[data-bo-bind="vehicle.pricing[vehicle.pricing.planID].netPrice | number"]').innerText),
                vin: node.querySelector('.vehicle-vin').innerText,
                year: node.querySelector('.model-year').innerText,
                model: node.querySelector('.model-trim').innerText,
                dealer: node.querySelector('.dealer-name').innerText,
                link: node.querySelector('.vehicle-title-link').getAttribute("href"),
            })
        })
        return __records;
    });

    console.log(`${zip.zip_code} found ${_records.length} records`)

    page.close();


    return _records;

}

async function get_all_cars() {
    let records = []
    for (let i = 0; i < zips.length; i++) {
        records = records.concat(await scrape_fords(zips[i]));
        writeZipjson(records, "./data/allCars.json");
    }
}

async function get_total_cars() {
    let records = []
    for (let i = 0; i < zips.length; i++) {
        const _zip = zips[i];
        const _cars = await scrape_fords(zips[i]);

        const _lariats = _cars.filter(_car => _car.model === "LARIAT");
        const _xlt = _cars.filter(_car => _car.model === "XLT");

        records.push({
            ..._zip,
            total_cars: _cars.length,
            lariat_count : _lariats.length,
            lariat_min: _lariats.reduce((min, _car) => _car.price < min ? _car.price: min,99999),
            xlt_count : _xlt.length,
            xlt_min: _xlt.reduce((min, _car) => _car.price < min ? _car.price: min,99999),
        })
        writeZipjson(records, "./data/totalCars.json");
    }
}

let zips = await readZipjson("./data/FilteredZips.json");
const browser = await puppeteer.launch({headless: false});
await get_total_cars();

await browser.close();


 */

