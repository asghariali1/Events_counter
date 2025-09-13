// Configuration for each counter with different time periods
        let counters = {
            'traffic-deaths': {
                dailyAverage: 60,
                monthlyAverage: 1800,
                yearlyAverage: 21900,
                current: 0,
            },
            'education-dropouts': {
                dailyAverage: 450,
                monthlyAverage: 13500,
                yearlyAverage: 164250,
                current: 0,
            },
            'pollution-deaths': {
                dailyAverage: 85,
                monthlyAverage: 2550,
                yearlyAverage: 31025,
                current: 0,
            },
            'workers-deaths': {
                dailyAverage: 5,
                monthlyAverage: 166,
                yearlyAverage: 1986,
                current: 0,
            },
            'unemployment-claims': {
                dailyAverage: 1200,
                monthlyAverage: 36000,
                yearlyAverage: 438000,
                current: 0,
            },
            'new-births': {
                dailyAverage: 3500,
                monthlyAverage: 105000,
                yearlyAverage: 1277500,
                current: 0,
            },
            'violence-against-women': {
                dailyAverage: 0.5,
                monthlyAverage: 15,
                yearlyAverage: 180,
                current: 0,
            },
            'soil-erosion': {
                dailyAverage: 42.2,
                monthlyAverage: 1283,
                yearlyAverage: 15400,
                current: 0,
            },
            'death-penalty': {
                dailyAverage: 0.1,
                monthlyAverage: 3,
                yearlyAverage: 36,
                current: 0,
            }
        };

        // Function to load statistics from JSON
        async function loadStatisticsFromJSON() {
            try {
                const response = await fetch('data/statistics.json');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                const stats = data.iran_statistics.statistics;
                
                // Update counters with data from JSON
                counters['traffic-deaths'] = {
                    dailyAverage: stats.traffic_accidents_deaths.deaths.daily_average,
                    monthlyAverage: stats.traffic_accidents_deaths.deaths.monthly_average,
                    yearlyAverage: stats.traffic_accidents_deaths.deaths.yearly_average,
                    current: 0,
                };
                
                counters['education-dropouts'] = {
                    dailyAverage: stats.education.dropouts.daily_average,
                    monthlyAverage: stats.education.dropouts.monthly_average,
                    yearlyAverage: stats.education.dropouts.yearly_average,
                    current: 0,
                };
                
                counters['pollution-deaths'] = {
                    dailyAverage: stats.air_pollution.deaths.daily_average,
                    monthlyAverage: stats.air_pollution.deaths.monthly_average,
                    yearlyAverage: stats.air_pollution.deaths.yearly_average,
                    current: 0,
                };
                
                counters['workers-deaths'] = {
                    dailyAverage: stats.workers.deaths.daily_average,
                    monthlyAverage: stats.workers.deaths.monthly_average,
                    yearlyAverage: stats.workers.deaths.yearly_average,
                    current: 0,
                };
                
                counters['unemployment-claims'] = {
                    dailyAverage: stats.employment.unemployment_claims.daily_average,
                    monthlyAverage: stats.employment.unemployment_claims.monthly_average,
                    yearlyAverage: stats.employment.unemployment_claims.yearly_average,
                    current: 0,
                };
                
                counters['new-births'] = {
                    dailyAverage: stats.demographics.births.daily_average,
                    monthlyAverage: stats.demographics.births.monthly_average,
                    yearlyAverage: stats.demographics.births.yearly_average,
                    current: 0,
                };
                
                counters['violence-against-women'] = {
                    dailyAverage: stats.social.violence_against_women_deaths.daily_average,
                    monthlyAverage: stats.social.violence_against_women_deaths.monthly_average,
                    yearlyAverage: stats.social.violence_against_women_deaths.yearly_average,
                    current: 0,
                };
                
                counters['soil-erosion'] = {
                    dailyAverage: stats.environment.soil_erosion.daily_average,
                    monthlyAverage: stats.environment.soil_erosion.monthly_average,
                    yearlyAverage: stats.environment.soil_erosion.yearly_average,
                    current: 0,
                };

                counters['death-penalty'] = {
                    dailyAverage: stats.death_penalty.daily_average,
                    monthlyAverage: stats.death_penalty.monthly_average,
                    yearlyAverage: stats.death_penalty.yearly_average,
                    current: 0,
                };

                console.log('Statistics loaded from JSON successfully');
                return data;
            } catch (error) {
                console.error('Error loading statistics from JSON:', error);
                console.log('Using default values...');
                return null;
            }
        }

        let currentPeriod = 'daily';
        let isRealTime = false;
        let updateInterval;
        let pageLoadTime = new Date();
        let statisticsData = null;
        let currentChart = null;
        let modalData = {};

        // Load modal data from JSON
        function loadModalDataFromJSON(data) {
            if (!data || !data.iran_statistics || !data.iran_statistics.details) return;
            
            const details = data.iran_statistics.details;
            const mapping = {
                'traffic-deaths': 'traffic_accidents_deaths',
                'education-dropouts': 'education_dropouts', 
                'pollution-deaths': 'air_pollution_deaths',
                'workers-deaths': 'workers_deaths',
                'unemployment-claims': 'unemployment_claims',
                'new-births': 'births',
                'violence-against-women': 'violence_against_women_deaths',
                'soil-erosion': 'soil_erosion',
                'death-penalty': 'death_penalty'
            };
            
        Object.keys(mapping).forEach(key => {
            const jsonKey = mapping[key];
            if (details[jsonKey]) {
                modalData[key] = {
                    title: details[jsonKey].title,
                    description: details[jsonKey].description,
                    sources: details[jsonKey].sources,
                    sourcesLinks: details[jsonKey].sources_links || null,
                    chartData: details[jsonKey].chartData,
                    chartYears: details[jsonKey].chartYears
                };
                
                // Add world data for traffic accidents, air pollution deaths, and workers deaths
                if ((key === 'traffic-deaths' || key === 'pollution-deaths' || key === 'workers-deaths') && details[jsonKey].world) {
                    modalData[key].worldData = details[jsonKey].world;
                    modalData[key].worldYears = details[jsonKey].world.chartYears;
                    
                    // Extract world sources data
                    modalData[key].worldSources = {};
                    Object.keys(details[jsonKey].world).forEach(countryKey => {
                        if (countryKey !== 'chartYears' && details[jsonKey].world[countryKey]) {
                            const countryData = details[jsonKey].world[countryKey];
                            modalData[key].worldSources[countryKey] = {
                                source: countryData.source,
                                sources_link: countryData.sources_link || []
                            };
                        }
                    });
                }
            }
        });
            
            console.log('Modal data loaded from JSON:', modalData);
        }

        // Persian calendar utilities
        function getIranTime() {
            // Get current time in Iran timezone
            const now = new Date();
            const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
            const iranTime = new Date(utc + (3.5 * 3600000)); // Iran is UTC+3:30
            return iranTime;
        }

        function gregorianToJalali(gy, gm, gd) {
            // Accurate Gregorian to Persian (Jalali) calendar conversion
            // Based on Kazimierz M. Borkowski's algorithm with corrections
            
            let jy, jm, jd;
            
            // Adjustments for Persian calendar epoch and leap years
            let g_y = gy - 1600;
            let g_m = gm - 1;
            let g_d = gd - 1;
            
            let g_day_no = 365 * g_y + Math.floor((g_y + 3) / 4) - Math.floor((g_y + 99) / 100) + Math.floor((g_y + 399) / 400);
            
            for (let i = 0; i < g_m; ++i) {
                g_day_no += [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][i];
            }
            
            if (g_m > 1) {
                let leap = ((gy % 4 === 0) && (gy % 100 !== 0)) || (gy % 400 === 0);
                if (leap) g_day_no++;
            }
            
            g_day_no += g_d;
            
            let j_day_no = g_day_no - 79;
            
            let j_np = Math.floor(j_day_no / 12053);
            j_day_no %= 12053;
            
            jy = 979 + 33 * j_np + 4 * Math.floor(j_day_no / 1461);
            j_day_no %= 1461;
            
            if (j_day_no >= 366) {
                jy += Math.floor((j_day_no - 1) / 365);
                j_day_no = (j_day_no - 1) % 365;
            }
            
            if (j_day_no < 186) {
                jm = 1 + Math.floor(j_day_no / 31);
                jd = 1 + (j_day_no % 31);
            } else {
                jm = 7 + Math.floor((j_day_no - 186) / 30);
                jd = 1 + ((j_day_no - 186) % 30);
            }
            
            return [jy, jm, jd];
        }

        function getPersianDate(date = null) {
            const iranTime = date || getIranTime();
            const [jy, jm, jd] = gregorianToJalali(iranTime.getFullYear(), iranTime.getMonth() + 1, iranTime.getDate());
            
            const monthNames = [
                'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
                'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
            ];
            
            return {
                year: jy,
                month: jm,
                day: jd,
                monthName: monthNames[jm - 1],
                formatted: `${jd} ${monthNames[jm - 1]} ${jy}`
            };
        }

        function getPersianTime(date = null) {
            const iranTime = date || getIranTime();
            const hours = iranTime.getHours().toString().padStart(2, '0');
            const minutes = iranTime.getMinutes().toString().padStart(2, '0');
            const seconds = iranTime.getSeconds().toString().padStart(2, '0');
            
            // Convert to Persian numerals
            const persianNumerals = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
            const persianTime = `${hours}:${minutes}:${seconds}`.replace(/\d/g, d => persianNumerals[parseInt(d)]);
            
            return persianTime;
        }

        // Period configuration
        const periodConfig = {
            'real-time': {
                label: 'شمارش زنده از زمان بارگذاری صفحه',
                multiplier: 1,
                updateFrequency: 1000,
                showProgress: true
            },
            'daily': {
                label: 'امروز تا این لحظه',
                multiplier: 1,
                updateFrequency: null,
                showProgress: false
            },
            'monthly': {
                label: 'این ماه تا این لحظه',
                multiplier: 30,
                updateFrequency: null,
                showProgress: false
            },
            'yearly': {
                label: 'امسال تا این لحظه',
                multiplier: 365,
                updateFrequency: null,
                showProgress: false
            }
        };

        // Calculate progress through current period
        function getProgressThroughPeriod(period) {
            const now = getIranTime();
            
            switch(period) {
                case 'real-time':
                    // Time since page loaded in seconds
                    return Math.max(0, (now - pageLoadTime) / 1000);
                    
                case 'daily':
                    // Progress through current day (0-1) using Iran time
                    const iranStartOfDay = new Date(now);
                    iranStartOfDay.setHours(0, 0, 0, 0);
                    const progress = (now - iranStartOfDay) / (24 * 60 * 60 * 1000);
                    return Math.max(0, Math.min(1, progress));
                    
                case 'monthly':
                    // Progress through current Persian month (0-1)
                    const persianDate = getPersianDate(now);
                    const daysInPersianMonth = persianDate.month <= 6 ? 31 : (persianDate.month <= 11 ? 30 : 29);
                    const monthProgress = (persianDate.day - 1) / daysInPersianMonth; // day-1 because day starts from 1
                    return Math.max(0, Math.min(1, monthProgress));
                    
                case 'yearly':
                    // Progress through current Persian year (0-1)
                    const currentPersian = getPersianDate(now);
                    // Calculate day of year in Persian calendar
                    let dayOfYear = 0;
                    for (let m = 1; m < currentPersian.month; m++) {
                        dayOfYear += m <= 6 ? 31 : 30;
                    }
                    dayOfYear += currentPersian.day - 1; // day-1 because day starts from 1
                    const yearProgress = dayOfYear / 365;
                    return Math.max(0, Math.min(1, yearProgress));
                    
                default:
                    return 1;
            }
        }

        // Initialize counters based on selected period
        function initializeCounters(period) {
            Object.keys(counters).forEach(id => {
                const counter = counters[id];
                
                if (period === 'real-time') {
                    // Real-time: start from 0 when page loads
                    counter.current = 0;
                } else {
                    // Progressive periods: show progress based on time elapsed
                    const progress = getProgressThroughPeriod(period);
                    const key = period + 'Average';
                    counter.current = Math.floor((counter[key] || counter.dailyAverage) * progress);
                }
                
                updateDisplay(id, counter.current, period);
            });
            
            updatePeriodLabels(period);
        }

        // Update display with animation
        function updateDisplay(id, value, period) {
            const element = document.getElementById(id);
            if (!element) {
                console.error(`Element with ID '${id}' not found`);
                return;
            }
            
            const formattedValue = value.toLocaleString('fa-IR');
            
            if (element.textContent !== formattedValue) {
                element.textContent = formattedValue;
                element.classList.add('counter-animation');
                setTimeout(() => element.classList.remove('counter-animation'), 600);
            }
        }

        // Update period labels and rates
        function updatePeriodLabels(period) {
            const config = periodConfig[period];
            
            Object.keys(counters).forEach(id => {
                const periodElement = document.getElementById(id + '-period');
                const rateElement = document.getElementById(id + '-rate');
                const counter = counters[id];
                
                if (!periodElement) {
                    console.error(`Period element with ID '${id}-period' not found`);
                    return;
                }
                if (!rateElement) {
                    console.error(`Rate element with ID '${id}-rate' not found`);
                    return;
                }
                
                // Update period description
                if (period === 'real-time') {
                    periodElement.textContent = `${config.label}`;
                } else {
                    const progress = getProgressThroughPeriod(period);
                    let progressText = '';
                    
                    if (period === 'daily') {
                        const iranTime = getIranTime();
                        const timeString = getPersianTime(iranTime);
                        progressText = `تا ساعت ${timeString}`;
                    } else if (period === 'monthly') {
                        const persianDate = getPersianDate();
                        progressText = `تا روز ${persianDate.day} ${persianDate.monthName}`;
                    } else if (period === 'yearly') {
                        const persianDate = getPersianDate();
                        const startOfYear = new Date();
                        startOfYear.setMonth(2, 21); // Approximate start of Persian year (March 21)
                        const dayOfYear = Math.floor((getIranTime() - startOfYear) / (24 * 60 * 60 * 1000)) + 1;
                        progressText = `تا روز ${Math.max(1, dayOfYear)} سال ${persianDate.year}`;
                    }
                    
                    periodElement.textContent = `${config.label} ${progressText}`;
                }
                
                // Update rate information
                let rateText = '';
                switch(period) {
                    case 'real-time':
                        rateText = `~${(counter.dailyAverage / (24 * 60 * 60)).toFixed(2)} در ثانیه`;
                        break;
                    case 'daily':
                        rateText = `~${counter.dailyAverage.toLocaleString('fa-IR')} در روز`;
                        break;
                    case 'monthly':
                        rateText = `~${counter.monthlyAverage.toLocaleString('fa-IR')} در ماه`;
                        break;
                    case 'yearly':
                        rateText = `~${counter.yearlyAverage.toLocaleString('fa-IR')} در سال`;
                        break;
                }
                rateElement.textContent = rateText;
            });
        }

        // Real-time counter updates
        function updateCountersRealTime() {
            if (!isRealTime) return;
            
            Object.keys(counters).forEach(id => {
                const counter = counters[id];
                const secondsSincePageLoad = getProgressThroughPeriod('real-time');
                const perSecondRate = counter.dailyAverage / (24 * 60 * 60);
                
                // Calculate expected count based on time elapsed
                counter.current = Math.floor(perSecondRate * secondsSincePageLoad);
                updateDisplay(id, counter.current, 'real-time');
            });

            // Update timestamp with corrected Iran time
            const iranTime = getIranTime();
            const timeString = getPersianTime(iranTime);
            const persianDate = getPersianDate(iranTime);
            document.getElementById('last-update').textContent = `${timeString} - ${persianDate.formatted}`;
        }

        // Update progressive counters for daily/monthly/yearly views
        function updateProgressiveCounters() {
            if (isRealTime) return;
            
            Object.keys(counters).forEach(id => {
                const counter = counters[id];
                const progress = getProgressThroughPeriod(currentPeriod);
                const key = currentPeriod + 'Average';
                const expectedCount = Math.floor((counter[key] || counter.dailyAverage) * progress);
                
                if (counter.current !== expectedCount) {
                    counter.current = expectedCount;
                    updateDisplay(id, counter.current, currentPeriod);
                }
            });
            
            // Update period labels to reflect current time
            updatePeriodLabels(currentPeriod);
        }

        // Handle period button clicks
        function setupPeriodButtons() {
            const buttons = document.querySelectorAll('.period-btn');
            
            buttons.forEach(button => {
                button.addEventListener('click', () => {
                    // Remove active class from all buttons
                    buttons.forEach(btn => btn.classList.remove('active'));
                    
                    // Add active class to clicked button
                    button.classList.add('active');
                    
                    // Update current period
                    const newPeriod = button.getAttribute('data-period');
                    currentPeriod = newPeriod;
                    isRealTime = newPeriod === 'real-time';
                    
                    // Clear existing interval
                    if (updateInterval) {
                        clearInterval(updateInterval);
                        updateInterval = null;
                    }
                    
                    // Initialize counters for new period
                    initializeCounters(newPeriod);
                    
                    // Start appropriate updates
                    if (isRealTime) {
                        updateInterval = setInterval(updateCountersRealTime, 1000);
                    } else {
                        // Update progressive counters every minute for daily/monthly/yearly
                        updateInterval = setInterval(updateProgressiveCounters, 60000);
                    }
                });
            });
        }

        // Modal functionality
        function openModal(counterId) {
            const modal = document.getElementById('detailModal');
            const data = modalData[counterId];
            const counter = counters[counterId];
            
            if (!data || !counter) return;
            
            // Update modal content
            document.getElementById('modal-title').textContent = data.title;
            document.getElementById('modal-daily-avg').textContent = counter.dailyAverage.toLocaleString('fa-IR');
            document.getElementById('modal-monthly-avg').textContent = counter.monthlyAverage.toLocaleString('fa-IR');
            document.getElementById('modal-yearly-avg').textContent = counter.yearlyAverage.toLocaleString('fa-IR');
            document.getElementById('modal-description-text').textContent = data.description;
            
            // Update sources
            const sourcesList = document.getElementById('modal-sources-list');
            sourcesList.innerHTML = '';
            
            // Add Iran sources
            data.sources.forEach((source, index) => {
                const li = document.createElement('li');
                
                // Check if we have source links and if there's a corresponding link for this source
                if (data.sourcesLinks && data.sourcesLinks[index]) {
                    const link = document.createElement('a');
                    link.href = data.sourcesLinks[index];
                    link.textContent = source;
                    link.target = '_blank';
                    link.rel = 'noopener noreferrer';
                    link.style.color = '#60a5fa';
                    link.style.textDecoration = 'none';
                    link.style.borderBottom = '1px solid #60a5fa';
                    link.style.transition = 'color 0.2s ease';
                    
                    // Add hover effect
                    link.addEventListener('mouseenter', () => {
                        link.style.color = '#93c5fd';
                    });
                    link.addEventListener('mouseleave', () => {
                        link.style.color = '#60a5fa';
                    });
                    
                    li.appendChild(link);
                } else {
                    li.textContent = source;
                }
                
                sourcesList.appendChild(li);
            });
            
            // Add world sources for traffic accidents, air pollution deaths, and workers deaths
            if ((counterId === 'traffic-deaths' || counterId === 'pollution-deaths' || counterId === 'workers-deaths') && data.worldSources) {
                // Add separator
                const separator = document.createElement('li');
                separator.style.fontWeight = 'bold';
                separator.style.marginTop = '15px';
                separator.style.color = '#d1d5db';
                separator.textContent = 'منابع سایر کشورها:';
                sourcesList.appendChild(separator);
                
                // Country name mapping for Persian display
                const countryNames = {
                    'Turkey': 'ترکیه',
                    'US': 'آمریکا',
                    'EU': 'اتحادیه اروپا',
                    'Germany': 'آلمان'
                };
                
                Object.keys(data.worldSources).forEach(country => {
                    const countrySourceData = data.worldSources[country];
                    if (countrySourceData && countrySourceData.sources_link && countrySourceData.sources_link.length > 0) {
                        countrySourceData.sources_link.forEach(link => {
                            if (link && link.trim() !== '') {
                                const li = document.createElement('li');
                                const anchor = document.createElement('a');
                                anchor.href = link;
                                anchor.target = '_blank';
                                anchor.rel = 'noopener noreferrer';
                                anchor.style.color = '#60a5fa';
                                anchor.style.textDecoration = 'none';
                                anchor.style.borderBottom = '1px solid #60a5fa';
                                anchor.style.transition = 'color 0.2s ease';
                                
                                anchor.textContent = `${countryNames[country] || country} - آمار رسمی`;
                                
                                // Add hover effect
                                anchor.addEventListener('mouseenter', () => {
                                    anchor.style.color = '#93c5fd';
                                });
                                anchor.addEventListener('mouseleave', () => {
                                    anchor.style.color = '#60a5fa';
                                });
                                
                                li.appendChild(anchor);
                                sourcesList.appendChild(li);
                            }
                        });
                    }
                });
            }
            
            // Create chart
            createChart(data.chartData, data.chartYears, data.title, counterId);
            
            // Show modal
            modal.style.display = 'block';
        }

        function closeModal() {
            const modal = document.getElementById('detailModal');
            modal.style.display = 'none';
            
            // Destroy existing chart
            if (currentChart) {
                currentChart.destroy();
                currentChart = null;
            }
        }

        function createChart(chartData, chartYears, title, counterId = null) {
            const ctx = document.getElementById('statisticsChart').getContext('2d');
            
            // Destroy existing chart
            if (currentChart) {
                currentChart.destroy();
            }
            
            // Convert Persian years to display format
            const persianYears = chartYears ? chartYears.map(year => year.toString()) : ['۱۳۹۸', '۱۳۹۹', '۱۴۰۰', '۱۴۰۱', '۱۴۰۲', '۱۴۰۳', '۱۴۰۴'];
            
            let datasets = [{
                label: 'ایران',
                data: chartData,
                borderColor: '#60a5fa',
                backgroundColor: 'rgba(96, 165, 250, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#60a5fa',
                pointBorderColor: '#1e40af',
                pointBorderWidth: 2,
                pointRadius: 6
            }];

            // Add world data for traffic accidents, air pollution deaths, and workers deaths
            if ((counterId === 'traffic-deaths' || counterId === 'pollution-deaths' || counterId === 'workers-deaths') && modalData[counterId] && modalData[counterId].worldData) {
                const worldData = modalData[counterId].worldData;
                const worldYears = modalData[counterId].worldYears;
                
                if (worldData.Turkey) {
                    datasets.push({
                        label: 'ترکیه',
                        data: worldData.Turkey.chartData,
                        borderColor: '#f59e0b',
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4,
                        pointBackgroundColor: '#f59e0b',
                        pointBorderColor: '#d97706',
                        pointBorderWidth: 2,
                        pointRadius: 5
                    });
                }
                
                if (worldData.US) {
                    datasets.push({
                        label: 'آمریکا',
                        data: worldData.US.chartData,
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4,
                        pointBackgroundColor: '#ef4444',
                        pointBorderColor: '#dc2626',
                        pointBorderWidth: 2,
                        pointRadius: 5
                    });
                }
                
                if (worldData.EU) {
                    datasets.push({
                        label: 'اتحادیه اروپا',
                        data: worldData.EU.chartData,
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4,
                        pointBackgroundColor: '#10b981',
                        pointBorderColor: '#059669',
                        pointBorderWidth: 2,
                        pointRadius: 5
                    });
                }
                
                if (worldData.Germany) {
                    datasets.push({
                        label: 'آلمان',
                        data: worldData.Germany.chartData,
                        borderColor: '#8b5cf6',
                        backgroundColor: 'rgba(139, 92, 246, 0.1)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4,
                        pointBackgroundColor: '#8b5cf6',
                        pointBorderColor: '#7c3aed',
                        pointBorderWidth: 2,
                        pointRadius: 5
                    });
                }
            }
            
            currentChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: persianYears,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#f4f4f5',
                                font: {
                                    family: 'Vazirmatn',
                                    size: 14
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            },
                            ticks: {
                                color: '#d1d5db',
                                font: {
                                    family: 'Vazirmatn'
                                }
                            }
                        },
                        y: {
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            },
                            ticks: {
                                color: '#d1d5db',
                                font: {
                                    family: 'Vazirmatn'
                                },
                                callback: function(value) {
                                    return value.toLocaleString('fa-IR');
                                }
                            }
                        }
                    }
                }
            });
        }

        function setupModalEvents() {
            // Add click events to stat cards
            const statCards = document.querySelectorAll('.stat-card');
            statCards.forEach(card => {
                card.addEventListener('click', (e) => {
                    // Find the counter ID from the card's number element
                    const numberElement = card.querySelector('.stat-number');
                    if (numberElement) {
                        const counterId = numberElement.id;
                        openModal(counterId);
                    }
                });
            });
            
            // Close modal events
            document.getElementById('closeModal').addEventListener('click', closeModal);
            document.getElementById('detailModal').addEventListener('click', (e) => {
                if (e.target.id === 'detailModal') {
                    closeModal();
                }
            });
            
            // Escape key to close modal
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    closeModal();
                }
            });
        }

        // Debug function to test time accuracy (can be called from browser console)
        window.testTimeAccuracy = function() {
            const iranTime = getIranTime();
            const persianDate = getPersianDate(iranTime);
            const persianTime = getPersianTime(iranTime);
            
            console.log('Current Iran Time:', iranTime);
            console.log('Persian Date:', persianDate);
            console.log('Persian Time:', persianTime);
            console.log('Gregorian Date for comparison:', iranTime.toLocaleDateString());
            console.log('Gregorian Time for comparison:', iranTime.toLocaleTimeString());
            
            return {
                iranTime,
                persianDate,
                persianTime,
                gregorianDate: iranTime.toLocaleDateString(),
                gregorianTime: iranTime.toLocaleTimeString()
            };
        };

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', async function() {
            // Load statistics from JSON first
            statisticsData = await loadStatisticsFromJSON();
            
            // Load modal data from JSON
            if (statisticsData) {
                loadModalDataFromJSON(statisticsData);
            }
            
            // Record page load time for real-time calculations
            pageLoadTime = getIranTime();
            
            setupPeriodButtons();
            setupModalEvents();
            initializeCounters('daily'); // Start with daily view
            
            // Start progressive updates for daily view
            updateInterval = setInterval(updateProgressiveCounters, 60000);
            
            // Update timestamp immediately
            const iranTime = getIranTime();
            const timeString = getPersianTime(iranTime);
            const persianDate = getPersianDate(iranTime);
            document.getElementById('last-update').textContent = `${timeString} - ${persianDate.formatted}`;
        });