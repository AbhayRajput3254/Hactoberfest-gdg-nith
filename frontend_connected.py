import flask
import requests

app = flask.Flask(__name__)

html='''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MessOS - Live Mess Tracker</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
        }
        .progress-transition {
            transition: width 0.5s ease-in-out, background-color 0.5s ease-in-out;
        }
        .toast {
            visibility: hidden;
            opacity: 0;
            transition: opacity 0.3s, visibility 0.3s;
        }
        .toast.show {
            visibility: visible;
            opacity: 1;
        }
    </style>
</head>
<body class="text-gray-800 antialiased min-h-screen flex flex-col">

    <header class="bg-indigo-600 text-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
            <div class="flex items-center gap-3">
                <i class="fa-solid fa-utensils text-2xl"></i>
                <h1 class="text-2xl font-bold tracking-tight">MessOS</h1>
            </div>
            <div class="text-sm bg-indigo-500 px-3 py-1 rounded-full font-medium shadow-inner hidden sm:block">
                <i class="fa-solid fa-circle text-green-400 text-xs mr-1 animate-pulse"></i> Live Demo Mode
            </div>
        </div>
    </header>

    <main class="flex-grow max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        <!-- Responsive Grid: 1 column on mobile (stacked), 2 columns on lg desktop (side-by-side) -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">

            <!-- ========================================== -->
            <!-- STUDENT VIEW SECTION                       -->
            <!-- ========================================== -->
            <section class="space-y-6">
                <div class="flex items-center gap-2 mb-2">
                    <i class="fa-solid fa-user-graduate text-indigo-600 text-xl"></i>
                    <h2 class="text-2xl font-bold text-gray-900">Student View</h2>
                </div>

                <!-- Live Crowd Card -->
                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 relative overflow-hidden">
                    <div class="absolute top-0 right-0 bg-red-100 text-red-600 text-xs font-bold px-3 py-1 rounded-bl-lg">LIVE</div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">Current Crowd Status</h3>
                    <p class="text-sm text-gray-500 mb-4" id="crowd-status-text">Moderate crowd. Short waiting time.</p>
                    
                    <div class="flex justify-between text-sm font-medium mb-1">
                        <span id="crowd-count-display">45 / 100 People</span>
                        <span id="crowd-percentage-display">45% Full</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-4 mb-2 overflow-hidden shadow-inner">
                        <div id="crowd-progress-bar" class="h-4 rounded-full progress-transition bg-green-500" style="width: 45%;"></div>
                    </div>
                </div>

                <!-- Today's Menu Card -->
                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-lg font-semibold text-gray-800">Today's Menu</h3>
                        <span class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-md" id="current-date"></span>
                    </div>

                    <div class="space-y-4">
                        <!-- Breakfast -->
                        <div class="p-4 rounded-xl border border-gray-100 bg-gray-50 flex gap-4 items-start">
                            <div class="bg-orange-100 text-orange-500 p-3 rounded-full flex-shrink-0">
                                <i class="fa-solid fa-mug-hot"></i>
                            </div>
                            <div>
                                <h4 class="font-semibold text-gray-800">Breakfast <span class="text-xs font-normal text-gray-500 ml-2" id="breakfast-time">7:30 AM - 9:30 AM</span></h4>
                                <p class="text-sm text-gray-600 mt-1" id="breakfast-items">Idli, Sambar, Coconut Chutney, Tea/Coffee</p>
                            </div>
                        </div>
                        <!-- Lunch -->
                        <div class="p-4 rounded-xl border border-gray-100 bg-gray-50 flex gap-4 items-start">
                            <div class="bg-yellow-100 text-yellow-600 p-3 rounded-full flex-shrink-0">
                                <i class="fa-solid fa-bowl-rice"></i>
                            </div>
                            <div>
                                <h4 class="font-semibold text-gray-800">Lunch <span class="text-xs font-normal text-gray-500 ml-2" id="lunch-time">12:30 PM - 2:30 PM</span></h4>
                                <p class="text-sm text-gray-600 mt-1" id="lunch-items">Rice, Dal Tadka, Paneer Masala, Roti, Salad</p>
                            </div>
                        </div>
                        <!-- Dinner -->
                        <div class="p-4 rounded-xl border border-gray-100 bg-gray-50 flex gap-4 items-start">
                            <div class="bg-indigo-100 text-indigo-500 p-3 rounded-full flex-shrink-0">
                                <i class="fa-solid fa-moon"></i>
                            </div>
                            <div>
                                <h4 class="font-semibold text-gray-800">Dinner <span class="text-xs font-normal text-gray-500 ml-2" id="dinner-time">7:30 PM - 9:30 PM</span></h4>
                                <p class="text-sm text-gray-600 mt-1" id="dinner-items">Fried Rice, Veg Manchurian, Tomato Soup</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Waste Report & Feedback Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <!-- Food Waste -->
                    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col justify-center items-center text-center">
                        <i class="fa-solid fa-leaf text-green-500 text-3xl mb-2"></i>
                        <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wide">Yesterday's Waste</h3>
                        <p class="text-2xl font-bold text-gray-900 mt-1" id="waste-display">12.5 kg</p>
                        <p class="text-xs text-gray-400 mt-2">Let's try to reduce this today!</p>
                    </div>

                    <!-- Feedback -->
                    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                        <h3 class="text-sm font-semibold text-gray-800 mb-2">Rate Your Meal</h3>
                        <div class="flex gap-2 text-2xl text-gray-300 mb-3 cursor-pointer" id="star-rating">
                            <i class="fa-solid fa-star hover:text-yellow-400 transition-colors" data-value="1"></i>
                            <i class="fa-solid fa-star hover:text-yellow-400 transition-colors" data-value="2"></i>
                            <i class="fa-solid fa-star hover:text-yellow-400 transition-colors" data-value="3"></i>
                            <i class="fa-solid fa-star hover:text-yellow-400 transition-colors" data-value="4"></i>
                            <i class="fa-solid fa-star hover:text-yellow-400 transition-colors" data-value="5"></i>
                        </div>
                        <button onclick="submitFeedback()" class="w-full bg-indigo-50 hover:bg-indigo-100 text-indigo-600 py-2 rounded-lg text-sm font-medium transition-colors">
                            Submit Feedback
                        </button>
                    </div>
                </div>
            </section>

            <!-- ========================================== -->
            <!-- STAFF DASHBOARD SECTION                    -->
            <!-- ========================================== -->
            <section class="space-y-6">
                <div class="flex items-center gap-2 mb-2 lg:mt-0 mt-8">
                    <i class="fa-solid fa-clipboard-user text-gray-600 text-xl"></i>
                    <h2 class="text-2xl font-bold text-gray-900">Staff Dashboard</h2>
                </div>

                <!-- Camera-driven Crowd Count -->
                <div class="bg-gray-800 rounded-2xl shadow-md p-6 text-white border border-gray-700">
                    <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
                        <i class="fa-solid fa-users"></i> Live Crowd Control
                    </h3>
                    <p class="text-sm text-gray-400 mb-6">Occupancy is updated automatically from the camera counter.</p>
                    <div class="flex items-center justify-center">
                        <div class="text-center">
                            <span class="block text-4xl font-bold" id="staff-crowd-count">0</span>
                            <span class="text-xs text-gray-400">Current occupancy</span>
                        </div>
                    </div>
                    <p id="camera-connection-status" class="text-center text-xs text-yellow-300 mt-4">Connecting to people counter...</p>
                    <!-- This hidden stream keeps the counter processing frames. -->
                    <img src="http://127.0.0.1:5001/video_feed" alt="" style="display:none">
                </div>

                <!-- Update Menu Form -->
                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Quick Update Menu</h3>
                    <div class="space-y-4">
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Select Meal</label>
                            <select id="meal-selector" class="w-full border border-gray-300 rounded-lg p-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                                <option value="breakfast">Breakfast</option>
                                <option value="lunch">Lunch</option>
                                <option value="dinner">Dinner</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Menu Items (comma separated)</label>
                            <input type="text" id="new-menu-items" placeholder="e.g., Poha, Jalebi, Milk" class="w-full border border-gray-300 rounded-lg p-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                        </div>
                        <button onclick="updateMenu()" class="w-full bg-gray-800 hover:bg-gray-900 text-white py-2 rounded-lg text-sm font-medium transition-colors shadow-sm">
                            Update Live Menu
                        </button>
                    </div>
                </div>

                <!-- Log Waste Form -->
                <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                    <h3 class="text-lg font-semibold text-gray-800 mb-4">Log Daily Food Waste</h3>
                    <div class="flex gap-3">
                        <div class="relative flex-grow">
                            <input type="number" id="waste-input" placeholder="Amount" class="w-full border border-gray-300 rounded-lg p-2 pl-3 pr-10 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none">
                            <span class="absolute right-3 top-2 text-sm text-gray-400">kg</span>
                        </div>
                        <button onclick="updateWaste()" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-sm whitespace-nowrap">
                            Save Log
                        </button>
                    </div>
                </div>

            </section>
        </div>
    </main>

    <!-- Custom Toast Notification -->
    <div id="toast" class="toast fixed bottom-6 right-6 bg-gray-900 text-white px-6 py-3 rounded-lg shadow-xl flex items-center gap-3 z-50">
        <i class="fa-solid fa-circle-check text-green-400"></i>
        <span id="toast-message" class="text-sm font-medium">Action completed!</span>
    </div>

    <script>
        // Global State
        const state = {
            crowd: 0,
            maxCapacity: 100,
            menu: {
                breakfast: "Idli, Sambar, Coconut Chutney, Tea/Coffee",
                lunch: "Rice, Dal Tadka, Paneer Masala, Roti, Salad",
                dinner: "Fried Rice, Veg Manchurian, Tomato Soup"
            },
            waste: 12.5
        };

        // Set Current Date
        const dateOptions = { weekday: 'long', month: 'short', day: 'numeric' };
        document.getElementById('current-date').textContent = new Date().toLocaleDateString('en-US', dateOptions);

        // Read occupancy from the camera counter through this Flask app.
        async function refreshCameraCount() {
            const status = document.getElementById('camera-connection-status');
            try {
                const response = await fetch('/api/counts', { cache: 'no-store' });
                if (!response.ok) throw new Error('Counter offline');
                const data = await response.json();
                state.crowd = Math.max(0, Math.min(state.maxCapacity, Number(data.total) || 0));
                renderCrowdUI();
                status.textContent = 'Camera connected — live updates active';
                status.className = 'text-center text-xs text-green-300 mt-4';
            } catch (error) {
                status.textContent = 'Counter offline. Start counting_people_connected.py first.';
                status.className = 'text-center text-xs text-red-300 mt-4';
            }
        }

        // Core Functions
        function initApp() {
            renderCrowdUI();
            renderMenuUI();
            renderWasteUI();
            setupStarRating();
            refreshCameraCount();
            setInterval(refreshCameraCount, 500);
        }

        function renderCrowdUI() {
            // Calculate percentage
            let percentage = Math.round((state.crowd / state.maxCapacity) * 100);
            
            // Constrain values just in case
            if (percentage < 0) percentage = 0;
            if (percentage > 100) percentage = 100;
            if (state.crowd < 0) state.crowd = 0;
            if (state.crowd > state.maxCapacity) state.crowd = state.maxCapacity;

            // Update Text Elements
            document.getElementById('crowd-count-display').textContent = `${state.crowd} / ${state.maxCapacity} People`;
            document.getElementById('crowd-percentage-display').textContent = `${percentage}% Full`;
            document.getElementById('staff-crowd-count').textContent = state.crowd;

            // Update Progress Bar Width and Color
            const progressBar = document.getElementById('crowd-progress-bar');
            const statusText = document.getElementById('crowd-status-text');
            
            progressBar.style.width = `${percentage}%`;
            
            // Remove existing color classes
            progressBar.classList.remove('bg-green-500', 'bg-yellow-500', 'bg-red-500');

            if (percentage < 50) {
                progressBar.classList.add('bg-green-500');
                statusText.textContent = "Plenty of seating available. Walk right in!";
                statusText.className = "text-sm mb-4 text-green-600 font-medium";
            } else if (percentage < 85) {
                progressBar.classList.add('bg-yellow-500');
                statusText.textContent = "Filling up fast. Moderate wait times.";
                statusText.className = "text-sm mb-4 text-yellow-600 font-medium";
            } else {
                progressBar.classList.add('bg-red-500');
                statusText.textContent = "Very crowded! Expect delays to find a seat.";
                statusText.className = "text-sm mb-4 text-red-600 font-medium";
            }
        }

        function renderMenuUI() {
            document.getElementById('breakfast-items').textContent = state.menu.breakfast;
            document.getElementById('lunch-items').textContent = state.menu.lunch;
            document.getElementById('dinner-items').textContent = state.menu.dinner;
        }

        function renderWasteUI() {
            document.getElementById('waste-display').textContent = `${state.waste} kg`;
        }

        // Crowd occupancy is controlled by the camera counter.

        function updateMenu() {
            const meal = document.getElementById('meal-selector').value;
            const newItems = document.getElementById('new-menu-items').value;
            
            if (newItems.trim() === "") {
                showToast("Please enter menu items");
                return;
            }

            state.menu[meal] = newItems;
            renderMenuUI();
            document.getElementById('new-menu-items').value = ""; // clear input
            showToast(`${meal.charAt(0).toUpperCase() + meal.slice(1)} menu updated successfully!`);
        }

        function updateWaste() {
            const wasteInput = document.getElementById('waste-input').value;
            
            if (wasteInput === "" || isNaN(wasteInput)) {
                showToast("Please enter a valid number");
                return;
            }

            state.waste = parseFloat(wasteInput).toFixed(1);
            renderWasteUI();
            document.getElementById('waste-input').value = ""; // clear input
            showToast("Food waste log updated!");
        }

        // Interactions (Student View)
        let currentRating = 0;
        function setupStarRating() {
            const stars = document.querySelectorAll('#star-rating i');
            stars.forEach(star => {
                star.addEventListener('click', (e) => {
                    currentRating = e.target.dataset.value;
                    // Reset all
                    stars.forEach(s => {
                        s.classList.remove('text-yellow-400', 'fa-solid');
                        s.classList.add('text-gray-300', 'fa-regular');
                    });
                    // Highlight selected
                    for(let i=0; i<currentRating; i++) {
                        stars[i].classList.remove('text-gray-300', 'fa-regular');
                        stars[i].classList.add('text-yellow-400', 'fa-solid');
                    }
                });
            });
        }

        function submitFeedback() {
            if (currentRating === 0) {
                showToast("Please select a star rating first.");
                return;
            }
            showToast(`Thank you for your ${currentRating}-star feedback!`);
            // Reset rating visually (optional, kept simple for demo)
        }

        // Utilities
        function showToast(message) {
            const toast = document.getElementById('toast');
            document.getElementById('toast-message').textContent = message;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2500);
        }

        document.addEventListener('DOMContentLoaded', initApp);
    </script>
</body>
</html>
'''

@app.route("/")
def dashboard_home():
    return flask.render_template_string(html)


@app.route("/api/counts")
def camera_counts():
    try:
        response = requests.get("http://127.0.0.1:5001/counts", timeout=1.5)
        response.raise_for_status()
        return flask.jsonify(response.json())
    except requests.RequestException:
        return flask.jsonify({"error": "People counter is offline"}), 503


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
