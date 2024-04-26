var calendar = new FullCalendar.Calendar(document.getElementById("calendar"), {
      contentHeight: 'auto',
      aspectRatio: 0.2,
      initialView: "dayGridMonth",
      headerToolbar: {
        start: 'title', // will normally be on the left. if RTL, will be on the right
        center: '',
        end: 'today prev,next' // will normally be on the right. if RTL, will be on the left
      },
      selectable: true,
      editable: true,
      initialDate: '2024-04-23',
      events: [
        {
          title: 'R.A.W. Workshops - Mushroom Identification with Sequoia',
          start: '2024-04-28',
          end: '2024-04-28',
          className: 'bg-gradient-danger'
        },
        {
          title: 'Merri Creek Nest Box Walk',
          start: '2024-04-27',
          end: '2024-04-27',
          className: 'bg-gradient-warning'
        },
        {
          title: 'Wild Things at Wurundjeri Walk with Tony Slater',
          start: '2024-04-27',
          end: '2024-04-27',
          className: 'bg-gradient-success'
        },
        {
          title: 'Quarterly Frog Survey in Yarran Dheran - Autumn 2024',
          start: '2024-04-28',
          end: '2024-04-28',
          className: 'bg-gradient-info'
        },
        {
          title: 'Biodiversity Blitz @ Bellbird Dell',
          start: '2024-04-28',
          end: '2024-04-28',
          className: 'bg-gradient-primary'
        },
        {
          title: 'The Insect World of Yarran Dheran with Ian Moodie',
          start: '2024-04-27',
          end: '2024-04-27',
          className: 'bg-gradient-danger'
        },
        {
          title: 'Creatures of the Night Spotlight Tour',
          start: '2024-05-25',
          end: '2024-05-25',
          className: 'bg-gradient-warning'
        },
        {
          title: 'The final countdown? Preparing for the Quantum Age',
          start: 'Tomorrow at 6:00 PM',
          end: 'Tomorrow at 6:00 PM',
          className: 'bg-gradient-success'
        },
        {
          title: 'Learn About Citizen Science - how to get involved in a BioBlitz',
          start: '2024-04-28',
          end: '2024-04-28',
          className: 'bg-gradient-info'
        },
        {
          title: 'Guided Nature Walk and Talk at Caulfield Racecourse Reserve',
          start: '2024-04-28',
          end: '2024-04-28',
          className: 'bg-gradient-primary'
        },
        {
          title: 'Fascinating Frogs in Yarran Dheran with Frank Gallagher',
          start: '2024-04-28',
          end: '2024-04-28',
          className: 'bg-gradient-danger'
        },
        {
          title: 'Simon Kirby - How humans got language: learning, culture & evolution',
          start: '2024-06-17',
          end: '2024-06-17',
          className: 'bg-gradient-warning'
        },
        {
          title: 'City Nature Challenge: Spotlighting Night (Sunday Night)',
          start: '2024-04-28',
          end: '2024-04-28',
          className: 'bg-gradient-success'
        },
        {
          title: 'Eucalypts of Bellbird Dell',
          start: '2024-05-25',
          end: '2024-05-25',
          className: 'bg-gradient-info'
        },
        {
          title: 'Generative Ecologies: Design Imaginaries with A.I - Workshop',
          start: '2024-06-01',
          end: '2024-06-01',
          className: 'bg-gradient-primary'
        },
        {
          title: 'Copy of Generative Ecologies: Design Imaginaries with A.I - Exhibition',
          start: '2024-06-01',
          end: '2024-06-01',
          className: 'bg-gradient-danger'
        },
        {
          title: 'City Nature Challenge 2024 Bushtucker walk and talk at Westmeadows',
          start: '2024-04-28',
          end: '2024-04-28',
          className: 'bg-gradient-warning'
        },
        {
          title: 'City Nature Challenge 2024 guided bushwalk into Broadmeadows Valley Park',
          start: '2024-04-29',
          end: '2024-04-29',
          className: 'bg-gradient-success'
        },
        {
          title: 'Drawing conversations from classical to AI',
          start: '2024-05-25',
          end: '2024-05-25',
          className: 'bg-gradient-info'
        },
        {
          title: 'Birds of Hume talk and walk',
          start: '2024-07-03',
          end: '2024-07-03',
          className: 'bg-gradient-primary'
        },
        {
          title: 'An evening with Caroline Pope- Animal Communicator @ Pakenham Library',
          start: '2024-05-10',
          end: '2024-05-10',
          className: 'bg-gradient-danger'
        },
        {
          title: 'Bridgewater Lake Wildlife Habitat Garden',
          start: '2024-06-18',
          end: '2024-06-18',
          className: 'bg-gradient-warning'
        },
        {
          title: 'City Nature Challenge 2024 bird & flora bushwalk at Mt Ridley NCR',
          start: '2024-04-27',
          end: '2024-04-27',
          className: 'bg-gradient-success'
        },
        {
          title: 'City Nature Challenge 2024 guided bushwalk into Wanginu Park, Sunbury',
          start: '2024-04-26',
          end: '2024-04-26',
          className: 'bg-gradient-info'
        },
        {
          title: 'Wildlife Photographer of the Year Exhibition',
          start: 'Today at 10:00 AM + 26 more',
          end: 'Today at 10:00 AM + 26 more',
          className: 'bg-gradient-primary'
        },
        {
          title: 'FREE Forest Teacher PD for Science and Geography Teachers by Gould League',
          start: '2024-05-02',
          end: '2024-05-02',
          className: 'bg-gradient-danger'
        },
        {
          title: 'Gresswell Forest Park Walk',
          start: '2024-04-28',
          end: '2024-04-28',
          className: 'bg-gradient-warning'
        },
        {
          title: 'Creatures of the Night Spotlight Tour',
          start: '2024-04-27',
          end: '2024-04-27',
          className: 'bg-gradient-info'
        },
        {
          title: 'Yarra Bend Park Walk',
          start: 'Sat, May 18, 10:00 AM + 2 more',
          end: 'Sat, May 18, 10:00 AM + 2 more',
          className: 'bg-gradient-primary'
        },
        {
          title: 'Bird Walk in Yarran Dheran',
          start: '2024-05-05',
          end: '2024-05-05',
          className: 'bg-gradient-danger'
        },
        {
          title: 'Fungi Guided Walk with Dr Sapphire McMullan-Fisher',
          start: '2024-05-25',
          end: '2024-05-25',
          className: 'bg-gradient-warning'
        },
        {
          title: 'Yarra Valley EcoVineyards ground covers seminar and hydroseeding demo',
          start: '2024-05-13',
          end: '2024-05-13',
          className: 'bg-gradient-success'
        },
        {
          title: 'Koala Conservation Day: Weeding and Wildlife Walk',
          start: '2024-05-04',
          end: '2024-05-04',
          className: 'bg-gradient-info'
        },
        {
          title: 'City Nature Challenge: Spotlighting Night',
          start: '2024-04-29',
          end: '2024-04-29',
          className: 'bg-gradient-primary'
        },
        {
          title: 'City Nature Challenge 2024 bird walk and water bug survey at Jacana Wetland',
          start: '2024-04-28',
          end: '2024-04-28',
          className: 'bg-gradient-danger'
        },
        {
          title: 'City Nature Challenge 2024  spot-light walk at Woodlands Historic Park',
          start: '2024-04-27',
          end: '2024-04-27',
          className: 'bg-gradient-warning'
        },
        {
          title: 'Mornington Peninsula EcoVineyards ground covers seminar & hydroseeding demo',
          start: '2024-05-15',
          end: '2024-05-15',
          className: 'bg-gradient-success'
        },
        {
          title: '3 Day Frame Drum Making Intensive',
          start: '2024-06-14',
          end: '2024-06-14',
          className: 'bg-gradient-info'
        },
        {
          title: 'Architectural Glass with Bruce Hutton',
          start: '2024-04-26',
          end: '2024-04-26',
          className: 'bg-gradient-primary'
        },
        {
          title: 'Australian Heritage Festival - Archaeology Panel and Dig - Como House',
          start: '2024-05-18',
          end: '2024-05-18',
          className: 'bg-gradient-success'
        },
        {
          title: 'Ice and Fire: Protecting Australias Heard and McDonald Islands  - Melb',
          start: '2024-05-01',
          end: '2024-05-01',
          className: 'bg-gradient-info'
        },
        {
          title: 'Waller House Open Day',
          start: 'Sun, May 5, 10:00 AM + 6 more',
          end: 'Sun, May 5, 10:00 AM + 6 more',
          className: 'bg-gradient-primary'
        },
        {
          title: 'Eastern Long-necked Turtles at Yarran Dheran',
          start: '2024-05-31',
          end: '2024-05-31',
          className: 'bg-gradient-danger'
        },
        {
          title: 'Heritage walk of Newport Lakes',
          start: '2024-04-28',
          end: '2024-04-28',
          className: 'bg-gradient-warning'
        },
        {
          title: 'Australian Heritage Festival - Significant Trees of Rippon Lea',
          start: 'Fri, May 3, 11:00 AM + 1 more',
          end: 'Fri, May 3, 11:00 AM + 1 more',
          className: 'bg-gradient-primary'
        },
        {
          title: 'Cleopatras Bling presents Usta - Melbourne Design Week',
          start: '2024-05-23',
          end: '2024-05-23',
          className: 'bg-gradient-danger'
        },
        {
          title: 'Aussie Bush Illustration with Jess Racklyeft',
          start: 'Sat, Jun 15, 11:00 AM + 1 more',
          end: 'Sat, Jun 15, 11:00 AM + 1 more',
          className: 'bg-gradient-success'
        },
        {
          title: 'Greenvale School Holidays Planting',
          start: '2024-07-08',
          end: '2024-07-08',
          className: 'bg-gradient-danger'
        },
        {
          title: 'HCG Wicking Beds Workshop',
          start: '2024-05-19',
          end: '2024-05-19',
          className: 'bg-gradient-warning'
        },
        {
          title: 'A Day Out—Art and Gardens',
          start: '2024-05-22',
          end: '2024-05-22',
          className: 'bg-gradient-success'
        },
        {
          title: 'Pareip / Pre Spring Walk on Country, around Jawbone Reserve',
          start: '2024-08-03',
          end: '2024-08-03',
          className: 'bg-gradient-info'
        },
        {
          title: 'Regenerative Urban farming',
          start: 'Tue, May 14, 11:00 AM + 1 more',
          end: 'Tue, May 14, 11:00 AM + 1 more',
          className: 'bg-gradient-primary'
        },
        {
          title: 'My Day of Days Exhibition - Mulberry Hill',
          start: '2024-04-28',
          end: '2024-04-28',
          className: 'bg-gradient-danger'
        },
        {
          title: 'Explore Jacks Magazine',
          start: '2024-06-02',
          end: '2024-06-02',
          className: 'bg-gradient-warning'
        },
        {
          title: 'Koala Food Tree Planting Day - Mount Martha',
          start: '2024-06-16',
          end: '2024-06-16',
          className: 'bg-gradient-success'
        },
        {
          title: 'NATIONAL TREE DAY - Koala Food Tree Planting Day - Moorooduc',
          start: '2024-07-28',
          end: '2024-07-28',
          className: 'bg-gradient-danger'
        },
        {
          title: 'The Birds of Altonas Coastal Wetlands - A Masterclass with Kevin Wood',
          start: '2024-02-17',
          end: '2024-02-17',
          className: 'bg-gradient-success'
        },
        {
          title: 'Indigenous Art and Printing at Nomad Gallery',
          start: '2024-04-27',
          end: '2024-04-27',
          className: 'bg-gradient-danger'
        },
        {
          title: 'Cloth Covered Solander Style Box',
          start: '2024-06-29',
          end: '2024-06-29',
          className: 'bg-gradient-warning'
        },
        {
          title: 'Printmaking with Dana Coleman',
          start: '2024-06-01',
          end: '2024-06-01',
          className: 'bg-gradient-success'
        },
        {
          title: 'Sculptural Forms from Nature with Katrina Carter',
          start: '2024-05-25',
          end: '2024-05-25',
          className: 'bg-gradient-info'
        },
      ],
      views: {
        month: {
          titleFormat: {
            month: "long",
            year: "numeric"
          }
        },
        agendaWeek: {
          titleFormat: {
            month: "long",
            year: "numeric",
            day: "numeric"
          }
        },
        agendaDay: {
          titleFormat: {
            month: "short",
            year: "numeric",
            day: "numeric"
          }
        }
      },
    });

    calendar.render();

    var ctx1 = document.getElementById("chart-line-1").getContext("2d");

    var gradientStroke1 = ctx1.createLinearGradient(0, 230, 0, 50);

    gradientStroke1.addColorStop(1, 'rgba(255,255,255,0.3)');
    gradientStroke1.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke1.addColorStop(0, 'rgba(203,12,159,0)'); //purple colors

    new Chart(ctx1, {
      type: "line",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
          label: "Visitors",
          tension: 0.5,
          borderWidth: 0,
          pointRadius: 0,
          borderColor: "#fff",
          borderWidth: 2,
          backgroundColor: gradientStroke1,
          data: [50, 45, 60, 60, 80, 65, 90, 80, 100],
          maxBarThickness: 6,
          fill: true
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
            },
            ticks: {
              display: false
            }
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
            },
            ticks: {
              display: false
            }
          },
        },
      },
    });