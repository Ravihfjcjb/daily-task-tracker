// Daily Task Tracker App

class TaskTracker {
    constructor() {
        this.tasks = [];
        this.completedDates = [];
        this.currentStreak = 0;
        this.bestStreak = 0;
        this.init();
    }

    init() {
        this.loadFromLocalStorage();
        this.setupEventListeners();
        this.updateUI();
        this.renderCalendar();
    }

    setupEventListeners() {
        document.getElementById('addTaskBtn').addEventListener('click', () => this.addTask());
        document.getElementById('taskInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTask();
        });
        document.getElementById('completeDayBtn').addEventListener('click', () => this.completeDay());
    }

    addTask() {
        const input = document.getElementById('taskInput');
        const taskText = input.value.trim();

        if (!taskText) {
            alert('Please enter an activity!');
            return;
        }

        const task = {
            id: Date.now(),
            text: taskText,
            completed: false,
            date: new Date().toISOString().split('T')[0]
        };

        this.tasks.push(task);
        input.value = '';
        this.saveToLocalStorage();
        this.updateUI();
    }

    deleteTask(id) {
        this.tasks = this.tasks.filter(task => task.id !== id);
        this.saveToLocalStorage();
        this.updateUI();
    }

    toggleTask(id) {
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            task.completed = !task.completed;
            this.saveToLocalStorage();
            this.updateUI();
        }
    }

    completeDay() {
        const today = new Date().toISOString().split('T')[0];

        if (this.completedDates.includes(today)) {
            alert('You have already completed today!');
            return;
        }

        if (this.tasks.filter(t => t.date === today).length === 0) {
            alert('Please add at least one activity before completing the day!');
            return;
        }

        this.completedDates.push(today);
        this.updateStreak();
        this.saveToLocalStorage();
        this.updateUI();
        this.showNotification('🎉 Great job! Day completed!');
    }

    updateStreak() {
        const sortedDates = [...this.completedDates].sort();
        let streak = 0;
        let maxStreak = 0;
        let lastDate = null;

        for (let date of sortedDates) {
            const currentDate = new Date(date);
            if (lastDate === null) {
                streak = 1;
            } else {
                const lastDateTime = new Date(lastDate);
                const diffDays = Math.floor((currentDate - lastDateTime) / (1000 * 60 * 60 * 24));
                if (diffDays === 1) {
                    streak++;
                } else {
                    maxStreak = Math.max(maxStreak, streak);
                    streak = 1;
                }
            }
            lastDate = date;
        }

        maxStreak = Math.max(maxStreak, streak);
        this.bestStreak = maxStreak;

        // Check if streak is still active (last completed date is today or yesterday)
        const today = new Date().toISOString().split('T')[0];
        const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
        
        if (this.completedDates.includes(today) || (this.completedDates.includes(yesterday) && this.currentStreak > 0)) {
            this.currentStreak = streak;
        } else if (this.completedDates.includes(yesterday)) {
            this.currentStreak = streak;
        } else {
            this.currentStreak = 0;
        }
    }

    showNotification(message) {
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #48bb78;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        document.body.appendChild(notification);

        setTimeout(() => notification.remove(), 3000);
    }

    updateUI() {
        this.updateTasksList();
        this.updateStats();
        this.renderCalendar();
    }

    updateTasksList() {
        const tasksList = document.getElementById('tasksList');
        const today = new Date().toISOString().split('T')[0];
        const todayTasks = this.tasks.filter(t => t.date === today);

        if (todayTasks.length === 0) {
            tasksList.innerHTML = '<p class="empty-state">No activities added yet. Start by adding your first activity!</p>';
            return;
        }

        tasksList.innerHTML = todayTasks.map(task => `
            <div class="task-item ${task.completed ? 'completed' : ''}">
                <input 
                    type="checkbox" 
                    ${task.completed ? 'checked' : ''} 
                    onchange="tracker.toggleTask(${task.id})"
                    style="margin-right: 12px; width: 18px; height: 18px; cursor: pointer;"
                >
                <span class="task-text">${this.escapeHtml(task.text)}</span>
                <div class="task-actions">
                    <button class="btn btn-danger" onclick="tracker.deleteTask(${task.id})">Delete</button>
                </div>
            </div>
        `).join('');
    }

    updateStats() {
        const today = new Date().toISOString().split('T')[0];
        const thisWeekStart = new Date(Date.now() - 7 * 86400000).toISOString().split('T')[0];
        const thisMonthStart = new Date(Date.now() - 30 * 86400000).toISOString().split('T')[0];

        const totalActivities = this.tasks.length;
        const thisWeek = this.completedDates.filter(d => d >= thisWeekStart).length;
        const thisMonth = this.completedDates.filter(d => d >= thisMonthStart).length;

        document.getElementById('streakCount').textContent = this.currentStreak;
        document.getElementById('totalActivities').textContent = totalActivities;
        document.getElementById('thisWeek').textContent = thisWeek;
        document.getElementById('thisMonth').textContent = thisMonth;
        document.getElementById('bestStreak').textContent = this.bestStreak;

        const lastCompleted = this.completedDates.length > 0 ? this.completedDates[this.completedDates.length - 1] : null;
        const lastUpdatedEl = document.getElementById('lastUpdated');
        if (lastCompleted) {
            const lastDate = new Date(lastCompleted);
            lastUpdatedEl.textContent = `Last updated: ${lastDate.toLocaleDateString()}`;
        }
    }

    renderCalendar() {
        const calendar = document.getElementById('calendar');
        const today = new Date();
        const year = today.getFullYear();
        const month = today.getMonth();

        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();
        const startingDayOfWeek = firstDay.getDay();

        let html = '';

        // Empty cells for days before month starts
        for (let i = 0; i < startingDayOfWeek; i++) {
            html += '<div class="calendar-day disabled"></div>';
        }

        // Days of the month
        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month, day);
            const dateStr = date.toISOString().split('T')[0];
            const isCompleted = this.completedDates.includes(dateStr);
            const isToday = dateStr === new Date().toISOString().split('T')[0];

            html += `
                <div class="calendar-day ${isCompleted ? 'completed' : ''} ${isToday ? 'today' : ''}">
                    ${day}
                </div>
            `;
        }

        calendar.innerHTML = html;
    }

    saveToLocalStorage() {
        localStorage.setItem('taskTrackerData', JSON.stringify({
            tasks: this.tasks,
            completedDates: this.completedDates,
            currentStreak: this.currentStreak,
            bestStreak: this.bestStreak
        }));
    }

    loadFromLocalStorage() {
        const data = localStorage.getItem('taskTrackerData');
        if (data) {
            const parsed = JSON.parse(data);
            this.tasks = parsed.tasks || [];
            this.completedDates = parsed.completedDates || [];
            this.currentStreak = parsed.currentStreak || 0;
            this.bestStreak = parsed.bestStreak || 0;
            this.updateStreak();
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app
const tracker = new TaskTracker();

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);