"""
Smart Travel Planner — RAG Knowledge Base
Populates ChromaDB with travel documents for 6 Indian destinations.
Run once: python knowledge_base.py
"""

import chromadb
from chromadb.config import Settings
import os
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "..", "data", "chroma_db")

# ─── Travel Documents ─────────────────────────────────────────────────────────

TRAVEL_DOCS = [
    # ── GOA ──────────────────────────────────────────────────────────────
    {
        "id": "goa_overview",
        "destination": "Goa",
        "category": "overview",
        "text": (
            "Goa is India's smallest state and most famous beach destination, located on the western coast. "
            "Known for its stunning beaches, Portuguese colonial architecture, vibrant nightlife, and delicious seafood. "
            "The best time to visit Goa is from November to February when the weather is pleasant and dry. "
            "Goa has two main regions: North Goa known for party beaches like Baga, Calangute, and Anjuna, "
            "and South Goa known for serene beaches like Palolem, Colva, and Agonda. "
            "The state attracts both domestic and international tourists year-round."
        ),
    },
    {
        "id": "goa_attractions",
        "destination": "Goa",
        "category": "attractions",
        "text": (
            "Top attractions in Goa: Baga Beach and Calangute Beach are the most popular in North Goa. "
            "Dudhsagar Waterfalls is a spectacular four-tiered waterfall near the Karnataka border. "
            "Basilica of Bom Jesus is a UNESCO World Heritage Site housing the mortal remains of St. Francis Xavier. "
            "Fort Aguada is a 17th-century Portuguese fort with panoramic sea views. "
            "Old Goa churches including Se Cathedral are must-visits for history lovers. "
            "Anjuna Flea Market on Wednesdays is perfect for shopping. "
            "Dolphin watching tours from Sinquerim Beach are popular activities. "
            "Spice plantation tours in Ponda offer authentic Goan experience."
        ),
    },
    {
        "id": "goa_food",
        "destination": "Goa",
        "category": "food",
        "text": (
            "Goan cuisine is a unique blend of Indian and Portuguese influences. "
            "Must-try dishes include Fish Curry Rice (the staple Goan meal), Prawn Balchão (spicy pickled prawn), "
            "Chicken/Pork Cafreal, Sorpotel (spicy pork dish), and Goan sausages. "
            "Bebinca is the traditional Goan dessert made from coconut milk and eggs. "
            "Feni is the local cashew or coconut spirit unique to Goa. "
            "Famous restaurants: Britto's at Baga Beach, Thalassa Greek Restaurant, Vinayak Family Restaurant in Porvorim. "
            "Beach shacks offer fresh seafood grilled on the spot. "
            "Budget meals cost ₹150–300 per person; fine dining ₹800–2000 per person."
        ),
    },
    {
        "id": "goa_budget",
        "destination": "Goa",
        "category": "budget",
        "text": (
            "Budget travel in Goa (per person per day): ₹1500–2500. "
            "Mid-range travel: ₹3000–5000 per person per day. "
            "Luxury travel: ₹8000–15000+ per person per day. "
            "Budget accommodation options include hostels (₹500–800/night) and guesthouses (₹1000–2000/night). "
            "Mid-range hotels: ₹2500–5000/night. Luxury resorts: ₹7000–20000+/night. "
            "Renting a scooter costs ₹300–500/day. Taxi from airport to North Goa: ₹700–1000. "
            "Entry fees: Most beaches are free. Dudhsagar jeep safari: ₹2500 per person. "
            "Spice plantation tour: ₹400–600 per person including lunch."
        ),
    },
    {
        "id": "goa_tips",
        "destination": "Goa",
        "category": "travel_tips",
        "text": (
            "Travel tips for Goa: Book accommodation in advance during peak season (Dec–Jan). "
            "Rent a scooter or bicycle for exploring local areas — it's the most economical option. "
            "Avoid visiting during monsoon season (June–September) as beaches are rough and many shacks close. "
            "Carry cash as many beach shacks don't accept cards. "
            "South Goa is more peaceful; North Goa is better for nightlife and water sports. "
            "Carry sunscreen, hats, and light cotton clothes. "
            "Respect local customs at churches and temples — dress modestly. "
            "Bargain at the Anjuna flea market for best prices. "
            "Book Dudhsagar waterfall jeep tours through official operators only."
        ),
    },

    # ── JAIPUR ───────────────────────────────────────────────────────────
    {
        "id": "jaipur_overview",
        "destination": "Jaipur",
        "category": "overview",
        "text": (
            "Jaipur, the Pink City, is the capital of Rajasthan and a major part of India's Golden Triangle. "
            "Founded in 1727 by Maharaja Sawai Jai Singh II, it is famous for its magnificent forts, palaces, "
            "vibrant bazaars, and rich cultural heritage. "
            "The best time to visit is October to March when the weather is cool and pleasant. "
            "Jaipur is well connected by air, rail, and road to all major Indian cities. "
            "The city is a UNESCO Creative City of Crafts and Folk Arts."
        ),
    },
    {
        "id": "jaipur_attractions",
        "destination": "Jaipur",
        "category": "attractions",
        "text": (
            "Top attractions in Jaipur: Amber Fort (Amer Fort) is the most iconic, a stunning hilltop fortress. "
            "Hawa Mahal (Palace of Winds) is Jaipur's most photographed monument with its 953 windows. "
            "City Palace is a royal complex housing museums and still partially a royal residence. "
            "Jantar Mantar is a UNESCO World Heritage astronomical observatory. "
            "Nahargarh Fort offers panoramic views of the city and is beautiful at sunset. "
            "Jal Mahal (Water Palace) in the middle of Man Sagar Lake is a scenic landmark. "
            "Albert Hall Museum houses an eclectic collection of Egyptian mummies, carpets, and artifacts. "
            "Chokhi Dhani village resort offers authentic Rajasthani culture, food and entertainment."
        ),
    },
    {
        "id": "jaipur_food",
        "destination": "Jaipur",
        "category": "food",
        "text": (
            "Jaipur is a food lover's paradise with authentic Rajasthani cuisine. "
            "Must-try dishes: Dal Baati Churma (the quintessential Rajasthani meal), "
            "Laal Maas (fiery red mutton curry), Gatte ki Sabzi, Ker Sangri, and Pyaaz Kachori. "
            "Ghevar is the traditional Rajasthani sweet, especially popular during Teej festival. "
            "Famous food streets: MI Road, Johari Bazaar, and Bapu Bazaar. "
            "Top restaurants: Laxmi Mishthan Bhandar (LMB) for sweets and Rajasthani thali, "
            "Chokhi Dhani for traditional dinner with cultural show, "
            "Suvarna Mahal at Rambagh Palace for fine dining. "
            "Budget meals: ₹100–250. Mid-range: ₹500–1000. Fine dining: ₹1500–3000."
        ),
    },
    {
        "id": "jaipur_budget",
        "destination": "Jaipur",
        "category": "budget",
        "text": (
            "Budget travel in Jaipur (per person per day): ₹1200–2000. "
            "Mid-range: ₹2500–4500 per person per day. Luxury: ₹8000–25000+ (heritage hotels). "
            "Budget hostels: ₹400–700/night. Budget guesthouses: ₹800–1500/night. "
            "Mid-range hotels: ₹2000–4000/night. Heritage palace hotels: ₹8000–40000+/night. "
            "Composite ticket for major attractions (Amber Fort, City Palace, etc.): ₹1000 (Indian tourists). "
            "Elephant ride at Amber Fort: ₹1100–1400 per elephant (carries 2 people). "
            "Auto-rickshaw within city: ₹50–150 per trip. Taxi for full day sightseeing: ₹1500–2500. "
            "Shopping at Johari Bazaar for gems and jewelry, Bapu Bazaar for textiles."
        ),
    },
    {
        "id": "jaipur_tips",
        "destination": "Jaipur",
        "category": "travel_tips",
        "text": (
            "Travel tips for Jaipur: Start your day early to visit Amber Fort before the crowds arrive. "
            "Bargain firmly at all bazaars — vendors expect it. "
            "Hire a local guide for forts to fully understand the history (₹300–500 for 2 hours). "
            "Carry water and stay hydrated, especially April–June when temperatures exceed 40°C. "
            "Beware of gem scams — do not buy stones from touts. "
            "The composite heritage ticket is good value if visiting multiple monuments. "
            "Take a sunset walk on the Nahargarh Fort ramparts for golden-hour photos. "
            "Jaipur airport has direct flights from Mumbai, Delhi, Bengaluru. "
            "Book hotel in old city area (near City Palace) for the most authentic experience."
        ),
    },

    # ── KERALA ───────────────────────────────────────────────────────────
    {
        "id": "kerala_overview",
        "destination": "Kerala",
        "category": "overview",
        "text": (
            "Kerala, known as God's Own Country, is one of India's most scenic and culturally rich states. "
            "Located in the southwestern tip of India, Kerala is famous for its backwaters, hill stations, "
            "pristine beaches, Ayurvedic treatments, and lush tea and spice plantations. "
            "The best time to visit is October to February for beach areas and September–February for hill stations. "
            "Major tourist areas include Kochi, Munnar, Alleppey (Alappuzha), Thekkady, Varkala, and Kovalam. "
            "Kerala has the highest literacy rate in India and excellent infrastructure for tourism."
        ),
    },
    {
        "id": "kerala_attractions",
        "destination": "Kerala",
        "category": "attractions",
        "text": (
            "Top attractions in Kerala: Alleppey Backwaters — houseboat cruises through emerald waterways lined with coconut palms. "
            "Munnar Hill Station — sprawling tea plantations, misty mountains, and Eravikulam National Park (Nilgiri Tahr). "
            "Fort Kochi — a charming colonial quarter with Chinese fishing nets, churches, and art galleries. "
            "Periyar Wildlife Sanctuary in Thekkady — boat safaris to spot elephants, tigers, and deer. "
            "Varkala Beach — dramatic red cliffs above the Arabian Sea, great for yoga retreats. "
            "Wayanad — waterfalls, tribal villages, and coffee plantations. "
            "Thrissur Pooram — the world's most spectacular elephant procession festival. "
            "Padmanabhaswamy Temple in Thiruvananthapuram — one of India's richest temples."
        ),
    },
    {
        "id": "kerala_food",
        "destination": "Kerala",
        "category": "food",
        "text": (
            "Kerala cuisine is characterized by the use of coconut, curry leaves, and spices. "
            "Must-try dishes: Appam with Stew (lacy rice pancakes with vegetable or chicken curry), "
            "Karimeen Pollichathu (pearl spot fish in banana leaf), Malabar Biryani, "
            "Sadya (elaborate vegetarian feast served on banana leaf — 26+ dishes), "
            "Puttu and Kadala Curry (steamed rice cylinders with black chickpea curry), "
            "Kerala Prawn Curry with coconut milk, and Beef Fry. "
            "Coconut toddy (palm wine) is the traditional local drink. "
            "Top restaurants: Dhe Puttu in Kochi, Dal Roti in Fort Kochi, Paragon in Calicut. "
            "Budget meals: ₹120–300. Mid-range: ₹400–900. Fine dining: ₹1200–2500."
        ),
    },
    {
        "id": "kerala_budget",
        "destination": "Kerala",
        "category": "budget",
        "text": (
            "Budget travel in Kerala (per person per day): ₹1500–2500. "
            "Mid-range: ₹3000–6000 per person per day. Luxury (resorts + houseboat): ₹8000–20000+. "
            "Budget guesthouses in Alleppey: ₹600–1200/night. "
            "Standard houseboat (2 bedrooms, 1 night, meals included): ₹8000–15000 per boat. "
            "Luxury houseboat: ₹18000–30000+ per night. "
            "Munnar budget homestays: ₹800–1500/night. Tea estate bungalows: ₹5000–10000/night. "
            "Periyar boat safari: ₹200–600 per person. "
            "Ayurvedic massage: ₹1500–3000 for 60-minute treatment. "
            "Kathakali dance performance tickets: ₹300–500."
        ),
    },
    {
        "id": "kerala_tips",
        "destination": "Kerala",
        "category": "travel_tips",
        "text": (
            "Travel tips for Kerala: Book houseboats well in advance, especially during October–January. "
            "Take overnight houseboats for the best experience — they include dinner and breakfast. "
            "Hire a self-drive car or bike in Munnar for maximum flexibility in tea gardens. "
            "Mosquito repellent is essential in backwater areas. "
            "Respect temple customs — non-Hindus may not be allowed inside some temples. "
            "Learn a few words of Malayalam — locals appreciate the effort. "
            "Visit Munnar during September–October for lush green tea gardens. "
            "Spice garden tours in Thekkady are free or nominally priced. "
            "Prefer DTPC (District Tourism Promotion Council) houseboats for safer and certified options."
        ),
    },

    # ── SHIMLA ───────────────────────────────────────────────────────────
    {
        "id": "shimla_overview",
        "destination": "Shimla",
        "category": "overview",
        "text": (
            "Shimla is the capital of Himachal Pradesh and the queen of Indian hill stations. "
            "Situated at an altitude of 2205 metres, it was the summer capital of British India. "
            "Known for its snow-covered peaks, toy train (Kalka–Shimla railway, UNESCO Heritage), "
            "Victorian architecture, colonial-era churches, and the iconic Mall Road. "
            "Best time to visit: March–June for pleasant weather, December–February for snowfall. "
            "Shimla is well connected by road from Delhi (370 km) and Chandigarh (115 km). "
            "The Kalka–Shimla narrow gauge railway is a UNESCO World Heritage Site."
        ),
    },
    {
        "id": "shimla_attractions",
        "destination": "Shimla",
        "category": "attractions",
        "text": (
            "Top attractions in Shimla: The Ridge — a large open space in the heart of the city with panoramic views. "
            "Mall Road — the main promenade lined with shops, cafes, and colonial buildings. "
            "Christ Church — one of the oldest churches in North India (1857). "
            "Jakhu Temple — hilltop Hanuman temple at 2455m with cable car access. "
            "Kufri — a mini hill station 13km from Shimla, popular for skiing and horse riding. "
            "Chadwick Falls — beautiful waterfall 7km from Shimla. "
            "Viceregal Lodge — stunning heritage building that housed British Viceroys. "
            "Narkanda — 65km from Shimla, known for apple orchards and Hatu Peak. "
            "Chail — 45km from Shimla, world's highest cricket ground."
        ),
    },
    {
        "id": "shimla_food",
        "destination": "Shimla",
        "category": "food",
        "text": (
            "Shimla's cuisine reflects Himachali mountain traditions. "
            "Must-try dishes: Sidu (local bread made from wheat flour, served with ghee), "
            "Chha Gosht (marinated lamb in yogurt gravy), Madra (chickpeas in yogurt sauce), "
            "Babru (local bread stuffed with black lentils), Tudkiya Bhath (rice cooked with lentils). "
            "Himachali dham (traditional festive meal) is a must if available during festivals. "
            "Street food: Bhutta (roasted corn), Maggi, and momos are popular on Mall Road. "
            "Famous restaurants: Indian Coffee House on Mall Road, Ashiana Restaurant (HPTDC), "
            "Café Sol, Baljees (famous for puri-chole). "
            "Budget meals: ₹100–200. Mid-range: ₹400–800. Fine dining: ₹1000–2000."
        ),
    },
    {
        "id": "shimla_budget",
        "destination": "Shimla",
        "category": "budget",
        "text": (
            "Budget travel in Shimla (per person per day): ₹1000–1800. "
            "Mid-range: ₹2000–4000 per person per day. Luxury: ₹6000–15000+. "
            "Budget guesthouses near Mall Road: ₹600–1200/night. "
            "Mid-range hotels: ₹2000–4000/night. Heritage hotels: ₹6000–15000/night. "
            "Kalka–Shimla toy train (Chair Car): ₹225 per person (5 hours, scenic). "
            "HRTC Volvo bus from Delhi: ₹700–1000 per person. "
            "Cable car to Jakhu: ₹250 up, ₹250 down. "
            "Kufri skiing charges: ₹500–800 per session in winter. "
            "Horse riding at Kufri: ₹500–1000 per round."
        ),
    },
    {
        "id": "shimla_tips",
        "destination": "Shimla",
        "category": "travel_tips",
        "text": (
            "Travel tips for Shimla: Book accommodation near Mall Road for easy access to all sights. "
            "Carry warm clothes even in summer — evenings get cold above 2000m. "
            "In winter (Dec–Feb), carry heavy woollens, gloves, and snow boots. "
            "The toy train journey from Kalka is one of India's most scenic — book in advance. "
            "Vehicles are not allowed on Mall Road — park at Lakkar Bazaar or Victory Tunnel. "
            "Apple season (August–October) is the best time for fresh local apples. "
            "Beware of monkeys at Jakhu Temple — keep bags closed and food hidden. "
            "Visit Kufri early morning to avoid crowds and get clear mountain views. "
            "Shimla becomes very crowded during summer school holidays — avoid peak weekends."
        ),
    },

    # ── ANDAMAN ──────────────────────────────────────────────────────────
    {
        "id": "andaman_overview",
        "destination": "Andaman",
        "category": "overview",
        "text": (
            "The Andaman and Nicobar Islands is a union territory of India located in the Bay of Bengal. "
            "Comprising over 572 islands, it is famous for its crystal-clear turquoise waters, "
            "white sand beaches, world-class snorkelling and scuba diving, tropical rainforests, "
            "and historical cellular jail from the British era. "
            "Port Blair is the capital and main entry point. "
            "Best time to visit: October to May (avoid June–September monsoons). "
            "The islands are accessible only by flight from Chennai, Kolkata, Delhi, or by ship."
        ),
    },
    {
        "id": "andaman_attractions",
        "destination": "Andaman",
        "category": "attractions",
        "text": (
            "Top attractions in Andaman: Radhanagar Beach on Havelock Island — rated Asia's best beach. "
            "Cellular Jail in Port Blair — national memorial for freedom fighters with light-and-sound show. "
            "Havelock Island (Swaraj Dweep) — the most popular tourist island for beaches and diving. "
            "Neil Island (Shaheed Dweep) — quiet, unspoilt beaches and coral reefs. "
            "Ross Island (Netaji Subhas Chandra Bose Island) — British-era ruins in a jungle setting. "
            "North Bay Island — water sports hub: glass-bottom boat rides, sea-walking, scuba diving. "
            "Baratang Island — limestone caves and mud volcanoes. "
            "Barren Island — South Asia's only active volcano, accessible by chartered boat."
        ),
    },
    {
        "id": "andaman_food",
        "destination": "Andaman",
        "category": "food",
        "text": (
            "Andaman cuisine is heavily influenced by Bengali, Tamil, Telugu, and Nicobarese traditions. "
            "Must-try dishes: Fresh seafood — grilled lobster, crab masala, prawn curry, fish tikka. "
            "Coconut-based curries with freshly caught fish. "
            "Coconut prawn curry and Amritsari fish fry are local favourites. "
            "South Indian breakfast (idli, dosa, vada) is widely available and excellent. "
            "Red snapper, tuna, and barracuda are commonly available fresh catches. "
            "Top restaurants: Full Moon Café on Havelock, Annapurna Cafeteria in Port Blair, "
            "Something Different restaurant on Neil Island. "
            "Budget meals: ₹150–350. Mid-range: ₹600–1200. "
            "Alcohol is available and reasonably priced compared to mainland India."
        ),
    },
    {
        "id": "andaman_budget",
        "destination": "Andaman",
        "category": "budget",
        "text": (
            "Budget travel in Andaman (per person per day): ₹2000–3500. "
            "Mid-range: ₹4000–7000 per person per day. Luxury: ₹10000–25000+. "
            "Flight from Chennai/Kolkata: ₹3000–8000 one-way per person. "
            "Government ferry from Port Blair to Havelock: ₹350–400 per person (2.5 hours). "
            "Private ferry (Makruzz/Nautika): ₹1500–2000 per person (faster, 1.5 hours). "
            "Budget guesthouses in Havelock: ₹800–1500/night. "
            "Mid-range resorts: ₹3000–6000/night. Luxury beach resorts: ₹10000–30000+/night. "
            "Scuba diving (beginner): ₹3500–5000 per dive. Advanced: ₹3000–4000. "
            "Sea walk: ₹3500 per person. Snorkelling: ₹1500–2000 per session."
        ),
    },
    {
        "id": "andaman_tips",
        "destination": "Andaman",
        "category": "travel_tips",
        "text": (
            "Travel tips for Andaman: Carry a photocopy of your ID — permits are required for some islands. "
            "Book ferry tickets in advance, especially during peak season (Dec–Jan). "
            "Avoid visiting restricted tribal areas (Jarawa and Sentinel territories). "
            "Carry biodegradable sunscreen to protect the coral reefs. "
            "Do not collect shells, corals, or marine life — it is illegal and harmful. "
            "ATMs are limited on Havelock and Neil islands — carry enough cash. "
            "Mobile network is spotty on outer islands — inform family before travelling. "
            "Book diving and snorkelling activities from PADI-certified operators only. "
            "Budget 3–4 days for Havelock alone to fully explore Radhanagar and Elephant Beach."
        ),
    },

    # ── LADAKH ───────────────────────────────────────────────────────────
    {
        "id": "ladakh_overview",
        "destination": "Ladakh",
        "category": "overview",
        "text": (
            "Ladakh is a union territory in northern India, often called the Land of High Passes. "
            "Situated in the trans-Himalayan region at altitudes between 2750m and 5600m, "
            "it is known for its stark, moon-like landscapes, Buddhist monasteries, pristine lakes, "
            "and the magnificent Zanskar and Indus river valleys. "
            "Best time to visit: June to September (roads are open, weather is pleasant). "
            "Leh is the main city and airport hub. Roads from Manali and Srinagar are open June–October. "
            "Inner Line Permits (ILP) are required to visit areas near the border."
        ),
    },
    {
        "id": "ladakh_attractions",
        "destination": "Ladakh",
        "category": "attractions",
        "text": (
            "Top attractions in Ladakh: Pangong Tso Lake — the world-famous high-altitude lake (4350m) "
            "straddling India and China, changing colours throughout the day. "
            "Nubra Valley — accessed via Khardung La (one of the world's highest motorable passes), "
            "famous for Bactrian camels and sand dunes at Hunder. "
            "Thiksey Monastery — 12-storey complex resembling Potala Palace in Tibet. "
            "Hemis Monastery — the largest and wealthiest monastery in Ladakh. "
            "Magnetic Hill — an optical illusion where cars appear to roll uphill. "
            "Leh Palace — ruined 17th-century palace with panoramic views. "
            "Zanskar Valley — remote valley for serious trekkers and river rafters. "
            "Tso Moriri — a high-altitude lake (4500m) with flamingos and bar-headed geese."
        ),
    },
    {
        "id": "ladakh_food",
        "destination": "Ladakh",
        "category": "food",
        "text": (
            "Ladakhi cuisine is Tibetan-influenced, warming, and high-calorie suited for mountain living. "
            "Must-try dishes: Thukpa (hearty noodle soup), Tsampa (roasted barley flour), "
            "Momos (steamed dumplings), Skyu (pasta in meat or vegetable broth), "
            "Chang (local barley beer), Butter Tea (po cha — salty tea with yak butter). "
            "Tingmo (steamed bread) served with curries is a local staple. "
            "Top restaurants in Leh: The Tibetan Kitchen, La Piazzetta, Bon Appetit, "
            "Gesmo Restaurant (legendary in Leh). "
            "Multicuisine cafes and Israeli food are popular near the main bazaar. "
            "Budget meals: ₹150–350. Mid-range: ₹400–900. "
            "Note: food options are limited outside Leh town."
        ),
    },
    {
        "id": "ladakh_budget",
        "destination": "Ladakh",
        "category": "budget",
        "text": (
            "Budget travel in Ladakh (per person per day): ₹1800–3000. "
            "Mid-range: ₹3500–6000 per person per day. Luxury camps: ₹8000–20000+. "
            "Flight from Delhi to Leh: ₹3500–10000 per person one-way. "
            "Budget guesthouses in Leh: ₹600–1200/night. "
            "Mid-range hotels: ₹2500–5000/night. Luxury heritage hotels: ₹8000–20000/night. "
            "Luxury glamping at Pangong: ₹5000–12000/night per tent. "
            "Taxi (Leh to Pangong Lake, shared): ₹3000–4000 per person. "
            "Royal Enfield rental: ₹1200–1800/day. "
            "Inner Line Permit (ILP) for Nubra/Pangong: ₹400 per person (group permit). "
            "River rafting on Zanskar: ₹1500–3000 per person."
        ),
    },
    {
        "id": "ladakh_tips",
        "destination": "Ladakh",
        "category": "travel_tips",
        "text": (
            "Travel tips for Ladakh: Acclimatize for at least 2 days in Leh before going to high-altitude areas. "
            "Do not go above 4000m within the first 24 hours of arrival — altitude sickness is serious. "
            "Carry Diamox (acetazolamide) — consult a doctor before taking. "
            "Stay well hydrated and avoid alcohol in the first two days. "
            "Apply high-SPF sunscreen (50+) — UV radiation is intense at altitude. "
            "Carry warm layers for evenings even in July — temperatures drop sharply at night. "
            "Inner Line Permits for Pangong, Nubra, and Tso Moriri can be obtained in Leh (takes 1–2 hours). "
            "Carry sufficient cash — ATMs are scarce and often out of service in remote areas. "
            "Fuel up at Leh — petrol stations are sparse on routes to Nubra and Pangong. "
            "Best season for the legendary Chadar Trek (frozen Zanskar river): January–February."
        ),
    },
]


def build_knowledge_base():
    """Load all travel documents into ChromaDB."""
    os.makedirs(CHROMA_PATH, exist_ok=True)

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Delete if exists to rebuild cleanly
    try:
        client.delete_collection("travel_knowledge")
        print("[INFO] Deleted existing collection")
    except Exception:
        pass

    collection = client.create_collection(
        name="travel_knowledge",
        metadata={"hnsw:space": "cosine"},
    )

    ids = [doc["id"] for doc in TRAVEL_DOCS]
    documents = [doc["text"] for doc in TRAVEL_DOCS]
    metadatas = [
        {"destination": doc["destination"], "category": doc["category"]}
        for doc in TRAVEL_DOCS
    ]

    collection.add(documents=documents, metadatas=metadatas, ids=ids)

    print(f"[SUCCESS] Added {len(TRAVEL_DOCS)} documents to ChromaDB")
    print(f"[INFO] Database location: {CHROMA_PATH}")
    return collection


def query_knowledge_base(query: str, destination: str = None, n_results: int = 3):
    """
    Query the ChromaDB collection.

    Args:
        query: Natural language query.
        destination: Optional filter by destination.
        n_results: Number of results to return.

    Returns:
        List of matching document texts.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection("travel_knowledge")

    where = None
    if destination:
        where = {"destination": destination}

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where,
    )

    return results["documents"][0] if results["documents"] else []


if __name__ == "__main__":
    build_knowledge_base()
    # Test query
    print("\n[TEST QUERY] Goa food recommendations:")
    results = query_knowledge_base("What food should I eat in Goa?", destination="Goa")
    for r in results:
        print(f"  → {r[:120]}...")
