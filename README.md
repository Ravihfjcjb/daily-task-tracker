# Daily Task Tracker 🏆

A beautiful and simple web app to track your daily tasks, maintain your streak, and monitor your activities.

## Features

✨ **Daily Task Management**
- Add your daily activities/tasks easily
- Mark tasks as complete
- Delete tasks you no longer need

🔥 **Streak Tracking**
- Automatically track your current streak
- View your best streak ever
- Maintain consistency with daily challenges

📅 **Calendar View**
- Visual calendar showing completed days
- See your progress at a glance
- Identify patterns in your productivity

📊 **Statistics Dashboard**
- Total activities logged
- Activities this week
- Activities this month
- Best streak record

💾 **Local Storage**
- All data is saved locally in your browser
- No server required
- Your data stays private

## How to Use

1. **Open** `index.html` in your web browser
2. **Add Activities** by typing in the input field and clicking "Add Activity" or pressing Enter
3. **Check Off** activities as you complete them
4. **Complete Day** by clicking the "Complete Today's Tasks" button once you're done
5. **Track Progress** by viewing your calendar and statistics

## File Structure

```
daily-task-tracker/
├── index.html      # Main HTML structure
├── styles.css      # Styling and responsive design
├── app.js          # JavaScript logic and functionality
└── README.md       # This file
```

## Features Explained

### Adding Tasks
- Type your daily activity in the input field
- Click "Add Activity" or press Enter
- Your activity appears in the "Today's Activities" section

### Completing the Day
- Add at least one activity
- Click "Complete Today's Tasks" when done
- Your streak will automatically update

### Viewing Statistics
- **Current Streak**: How many consecutive days you've completed tasks
- **Total Activities**: All activities ever logged
- **This Week**: Days completed in the last 7 days
- **This Month**: Days completed in the last 30 days
- **Best Streak**: Your longest streak ever

### Calendar
- Green days = completed tasks for that day
- Today's date has a blue border
- Grayed out dates = dates not yet in the month

## Customization

You can customize the app by:

1. **Colors**: Edit the CSS variables in `styles.css` under `:root`
2. **Text**: Change any label or placeholder text in `index.html`
3. **Layout**: Modify the CSS grid and flexbox properties

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Data Privacy

All your data is stored locally in your browser's localStorage. No data is sent to any server.

## Future Enhancements

- [ ] Dark mode toggle
- [ ] Export data as CSV
- [ ] Categories for different types of activities
- [ ] Reminders/notifications
- [ ] Weekly/Monthly goals
- [ ] Data backup to cloud

## License

Free to use and modify!

---

**Start tracking your daily activities today and build your streak! 🚀**