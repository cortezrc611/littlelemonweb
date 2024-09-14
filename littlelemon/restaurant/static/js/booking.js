document.addEventListener('DOMContentLoaded', function() {
    const bookedTimes = JSON.parse(document.getElementById('booked_times').dataset.times);
    const selectElement = document.getElementById('reservation_time');

    if (selectElement) {
        Array.from(selectElement.options).forEach(option => {
            if (bookedTimes.includes(option.value)) {
                option.disabled = true;
            }
        });
    }
});
