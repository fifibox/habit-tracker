// Function to create GitHub-style contribution grid cells from backend data
function generateGridCells(containerId, year, habitData) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    // Create 12 months (columns)
    for (let month = 0; month < 12; month++) {
        const column = document.createElement('div');
        column.className = 'grid-column';
        
        // Determine days in each month for the given year
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        
        // Create cells for each day
        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month, day);
            const dayOfWeek = date.getDay(); // 0 is Sunday, 1 is Monday, etc.
            
            // Only show cells for Monday (1), Wednesday (3), and Friday (5)
            const relevantDays = {
                'monday-grid': 1,
                'wednesday-grid': 3,
                'friday-grid': 5,
                'monday-grid-water': 1,
                'wednesday-grid-water': 3,
                'friday-grid-water': 5,
                'monday-grid-takeout': 1,
                'wednesday-grid-takeout': 3,
                'friday-grid-takeout': 5,
                'monday-grid-meditate': 1,
                'wednesday-grid-meditate': 3,
                'friday-grid-meditate': 5
            };
            
            if (dayOfWeek === relevantDays[containerId]) {
                const cell = document.createElement('div');
                cell.className = 'grid-cell';
                
                // Format date as YYYY-MM-DD for lookup
                const formattedDate = `${year}-${(month + 1).toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
                
                // Check if we have data for this date in our habitData
                if (habitData && habitData[formattedDate]) {
                    const intensity = habitData[formattedDate].intensity;
                    if (intensity > 0) {
                        cell.classList.add(`cell-level-${intensity}`);
                    }
                    
                    // Add tooltip with notes if available
                    if (habitData[formattedDate].notes) {
                        cell.setAttribute('title', habitData[formattedDate].notes);
                    }
                }
                
                column.appendChild(cell);
            }
        }
        
        container.appendChild(column);
    }
}

// Function to fetch habit data from backend
async function fetchHabitData(habitId, year) {
    try {
        // Make API request to get habit data for the specified year
        const response = await fetch(`/api/habits/${habitId}/data?year=${year}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching data for habit ${habitId}:`, error);
        return {}; // Return empty object on error
    }
}

// Function to fetch all habits from the backend
async function fetchHabits() {
    try {
        const response = await fetch('/api/habits');
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching habits:', error);
        return []; // Return empty array on error
    }
}

// Function to get habit mappings dynamically
async function getHabitMappings() {
    try {
        const habits = await fetchHabits();
        
        if (habits.length === 0) {
            // Fall back to default mappings if no habits found
            return defaultHabitMappings;
        }
        
        // Create custom mappings based on habit names
        return habits.map(habit => {
            const name = habit.name.toLowerCase();
            let suffix = '';
            
            if (name.includes('water') || name.includes('drink')) {
                suffix = '-water';
            } else if (name.includes('takeout') || name.includes('take out')) {
                suffix = '-takeout';
            } else if (name.includes('meditate') || name.includes('meditation')) {
                suffix = '-meditate';
            }
            
            return {
                id: habit.id,
                name: habit.name,
                grids: [
                    `monday-grid${suffix}`,
                    `wednesday-grid${suffix}`,
                    `friday-grid${suffix}`
                ]
            };
        });
    } catch (error) {
        console.error('Error creating habit mappings:', error);
        return defaultHabitMappings;
    }
}

// Default mappings to use as fallback
const defaultHabitMappings = [
    {
        id: 1, 
        name: "Wake up early",
        grids: ["monday-grid", "wednesday-grid", "friday-grid"]
    },
    {
        id: 2, 
        name: "Drink water",
        grids: ["monday-grid-water", "wednesday-grid-water", "friday-grid-water"]
    },
    {
        id: 3, 
        name: "No take out",
        grids: ["monday-grid-takeout", "wednesday-grid-takeout", "friday-grid-takeout"]
    },
    {
        id: 4, 
        name: "Meditate",
        grids: ["monday-grid-meditate", "wednesday-grid-meditate", "friday-grid-meditate"]
    }
];

// Initialize all grids with backend data
async function initializeGrids(year, habitMappings) {
    // If no mappings provided, use default mappings
    const mappings = habitMappings || defaultHabitMappings;
    
    // Show loading state (optional)
    const gridContainers = document.querySelectorAll('.grid-cells');
    gridContainers.forEach(container => {
        container.innerHTML = '<div class="loading">Loading data...</div>';
    });
    
    // Fetch and display data for each habit
    for (const habit of mappings) {
        try {
            // Fetch data for this habit
            const habitData = await fetchHabitData(habit.id, year);
            
            // Update all grid elements for this habit
            for (const gridId of habit.grids) {
                const container = document.getElementById(gridId);
                if (container) {
                    generateGridCells(gridId, year, habitData);
                }
            }
        } catch (error) {
            console.error(`Failed to initialize habit ${habit.name}:`, error);
            
            // Show error in grid
            for (const gridId of habit.grids) {
                const container = document.getElementById(gridId);
                if (container) {
                    container.innerHTML = '<div class="error">Failed to load data</div>';
                }
            }
        }
    }
}

// Year toggle functionality
document.addEventListener('DOMContentLoaded', async function() {
    // First get dynamic habit mappings
    const habitMappings = await getHabitMappings();
    
    // Handle year button clicks
    document.querySelectorAll('.year-button').forEach(button => {
        button.addEventListener('click', function() {
            const year = parseInt(this.getAttribute('data-year'));
            
            // Update active button
            document.querySelectorAll('.year-button').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
            
            // Regenerate grids with selected year
            initializeGrids(year, habitMappings);
        });
    });
    
    // Initialize with 2025 (default active year)
    initializeGrids(2025, habitMappings);
    
    // Share button functionality
    document.querySelectorAll('.share-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            // Get the habit name from the closest heading
            const habitTitle = this.closest('.habit-header')?.querySelector('.habit-title')?.textContent || 'this habit';
            
            // In a real app, you might generate a sharing link or open a dialog
            alert(`Share your progress for "${habitTitle}"`);
            
            // Example of what a real sharing feature might do:
            // 1. Generate a unique sharing URL
            // 2. Copy to clipboard or open sharing dialog
            // const shareUrl = `${window.location.origin}/share/habit/${habitId}`;
            // navigator.clipboard.writeText(shareUrl);
        });
    });
});