
const DAY_HEIGHT = "12vh";

export const calendar_style = {
    title: {
        display: "flex",
        m: -3,
        p: -3,
        justifyContent: "center"
    },
    border: {
        display: "flex",
        m: 3,
        p: 2,
        justifyContent: "center"
    },
    grid: {
        width: 1,
        gap: "7px"
    },
    gridItem: {
        width: 1,
    },
    day: {
        display: "flex",
        flexDirection: 'row',
        justifyContent: "space-between",
        width: 1,
        height: DAY_HEIGHT,
        border: 2,
        color: "lightGrey",
        '&:hover': {
            color: "grey",
            background: 'rgba(0, 0, 0, 0.02)'
        },
    },
    day_disabled: {
        display: "flex",
        flexDirection: 'column',
        width: 1,
        height: DAY_HEIGHT,
        background: "lightGrey"
    },

    day_selected: {
        display: "flex",
        flexDirection: 'row',
        justifyContent: "space-between",
        width: 1,
        height: DAY_HEIGHT,
        border: 3,
        color: "blue",
        '&:hover': {
            color: "blue",
            background: 'rgba(0, 0, 0, 0.02)'
        },
    },

    details: {
        display: 'flex',
        justifyContent: "left",
        p: 1,
    },
}

export const thermometer_style = {
    container: {
        display: "flex",
        m: "2%",
        position: "relative",
        width: "25px",
        height: "90%",
    },
    tube: {
        position: "absolute",
        top: 0,
        left: "27%",
        width: "48%",
        height: "80%",
        background: "black"
    },
    tube_inner: {
        position: "absolute",
        display: "flex",
        justifyContent: "end",
        flexDirection: 'column',
        top: "2%",
        left: "34%",
        width: "34%",
        height: "75%",
        background: "white"
    },
    tube_fill: {
        width: 1,
        height: 1,
        background: "white"
    },
    bulb: {
        position: "absolute",
        top: "70%",
        left: 0,
        width: 1,
        height: "30%",
        borderRadius: '50%',
        background: "black"
    },
    bulb_inner: {
        position: "absolute",
        top: "70%",
        left: "12%",
        width: 0.75,
        height: .28,
        borderRadius: '50%',
        background: "white"
    },

}

export const details_style = {
    text_field: {
        width: "240px"
    },
    date: {
        display: 'flex',
        justifyContent: "left",
        width: "20px",
        height: "20px"
    },
}