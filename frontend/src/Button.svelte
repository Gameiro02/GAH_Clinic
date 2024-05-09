<script>
    export let text = "BUTTON";
</script>

<button>
    <span>{text}</span>
</button>

<style>
    button {
        --bg: #62B6CB; /* Updated background color */
        --text-color: #fff; /* White text color remains */
        position: relative;
        width: 150px;
        border: none;
        background: var(--bg);
        color: var(--text-color);
        padding: 1em;
        font-weight: bold;
        text-transform: uppercase;
        transition: 0.2s;
        border-radius: 5px;
        opacity: 0.8;
        letter-spacing: 1px;
        box-shadow: #4a99ae 0px 7px 2px, #000 0px 8px 5px; /* Slightly lighter shade for shadow */
    }

    button:hover {
        opacity: 1;
    }

    button:active {
        top: 4px;
        box-shadow: #4a99ae 0px 3px 2px, #000 0px 3px 5px; /* Updated active state shadow */
    }
</style>

    