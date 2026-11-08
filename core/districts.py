"""Static geography: districts, approximate Indus main stem, barrages, basin bounds.

Coordinates are district HQ / city centres (approximate). The Indus path is a
schematic centre-line through known towns and barrages, NOT survey-grade data.
For exact river geometry, use GEE/HydroSHEDS in a later component.
"""
from dataclasses import dataclass

ALL_BASIN = "Indus Basin (overview)"
# (south-west, north-east) corner used to frame the whole basin in Pakistan
BASIN_BOUNDS = ((23.5, 66.0), (37.2, 77.8))


@dataclass(frozen=True)
class District:
    name: str
    province: str
    lat: float
    lon: float
    river: str  # main river / hazard context


def _d(name, prov, lat, lon, river):
    return District(name, prov, lat, lon, river)


_KP, _PB, _SD, _BL, _GB, _AJK = (
    "Khyber Pakhtunkhwa", "Punjab", "Sindh", "Balochistan", "Gilgit-Baltistan", "Azad Kashmir",
)

DISTRICTS: dict[str, District] = {
    d.name: d
    for d in [
        # Khyber Pakhtunkhwa
        _d("Nowshera", _KP, 34.0153, 71.9747, "Kabul River"),
        _d("Charsadda", _KP, 34.1453, 71.7308, "Kabul / Swat rivers"),
        _d("Peshawar", _KP, 34.0151, 71.5249, "Kabul River"),
        _d("Swat (Mingora)", _KP, 34.7717, 72.3600, "Swat River"),
        _d("Chitral", _KP, 35.8518, 71.7864, "Chitral River"),
        _d("Mardan", _KP, 34.1989, 72.0231, "Kalpani stream"),
        _d("Swabi", _KP, 34.1200, 72.4700, "Indus / Kabul"),
        _d("Kohistan (Dassu)", _KP, 35.2900, 73.2200, "Indus River"),
        _d("Dera Ismail Khan", _KP, 31.8626, 70.9019, "Indus; hill torrents"),
        _d("Bannu", _KP, 32.9889, 70.6056, "Kurram River"),
        _d("Abbottabad", _KP, 34.1558, 73.2194, "Dor / Haro streams"),
        # Punjab
        _d("Attock", _PB, 33.7667, 72.3667, "Indus / Kabul confluence"),
        _d("Mianwali", _PB, 32.5839, 71.5370, "Indus River"),
        _d("Layyah", _PB, 30.9693, 70.9427, "Indus River"),
        _d("Dera Ghazi Khan", _PB, 30.0489, 70.6455, "Hill torrents"),
        _d("Muzaffargarh", _PB, 30.0703, 71.1933, "Indus / Chenab"),
        _d("Rajanpur", _PB, 29.1044, 70.3302, "Hill torrents; Indus"),
        _d("Rahim Yar Khan", _PB, 28.4202, 70.2952, "Indus River"),
        _d("Multan", _PB, 30.1575, 71.5249, "Chenab"),
        _d("Bahawalpur", _PB, 29.3956, 71.6836, "Sutlej"),
        _d("Jhang", _PB, 31.2681, 72.3181, "Chenab / Jhelum"),
        _d("Sialkot", _PB, 32.4945, 74.5229, "Chenab tributaries"),
        _d("Gujranwala", _PB, 32.1877, 74.1945, "Chenab"),
        _d("Lahore", _PB, 31.5497, 74.3436, "Ravi"),
        _d("Rawalpindi", _PB, 33.5651, 73.0169, "Nullah Leh"),
        # Sindh
        _d("Kashmore", _SD, 28.4326, 69.5835, "Indus (Guddu)"),
        _d("Jacobabad", _SD, 28.2769, 68.4514, "Low-lying; drainage"),
        _d("Shikarpur", _SD, 27.9556, 68.6382, "Indus left/right bank"),
        _d("Sukkur", _SD, 27.7052, 68.8574, "Indus (Sukkur Barrage)"),
        _d("Khairpur", _SD, 27.5295, 68.7592, "Indus left bank"),
        _d("Larkana", _SD, 27.5589, 68.2264, "Indus right bank"),
        _d("Naushahro Feroze", _SD, 26.8400, 68.1200, "Indus"),
        _d("Dadu", _SD, 26.7319, 67.7750, "Manchar Lake; hill torrents"),
        _d("Sanghar", _SD, 26.0462, 68.9481, "Nara canal"),
        _d("Hyderabad", _SD, 25.3960, 68.3578, "Indus (Kotri)"),
        _d("Badin", _SD, 24.6560, 68.8370, "Coastal; drainage"),
        _d("Thatta", _SD, 24.7461, 67.9236, "Indus delta"),
        _d("Karachi", _SD, 24.8607, 67.0011, "Urban flooding; Lyari/Malir"),
        # Balochistan
        _d("Quetta", _BL, 30.1798, 66.9750, "Flash floods"),
        _d("Nasirabad (Dera Murad Jamali)", _BL, 29.1900, 68.2300, "Pat Feeder / Nari"),
        _d("Jaffarabad (Dera Allah Yar)", _BL, 28.3800, 68.3300, "Pat Feeder"),
        _d("Lasbela (Uthal)", _BL, 25.8070, 66.6190, "Hub / Porali rivers"),
        # Gilgit-Baltistan & AJK
        _d("Gilgit", _GB, 35.9208, 74.3083, "Gilgit River; GLOF risk"),
        _d("Skardu", _GB, 35.2971, 75.6333, "Indus; GLOF risk"),
        _d("Diamer (Chilas)", _GB, 35.4130, 74.0960, "Indus River"),
        _d("Muzaffarabad", _AJK, 34.3700, 73.4711, "Jhelum / Neelum"),
    ]
}

# Approximate Indus main stem, upstream -> downstream, (lat, lon)
INDUS_PATH = [
    (34.93, 76.20), (35.28, 75.60), (35.50, 75.10), (35.73, 74.62), (35.42, 74.10),
    (35.29, 73.22), (34.92, 72.88), (34.09, 72.70), (33.90, 72.25), (33.50, 71.90),
    (32.96, 71.55), (32.58, 71.55), (32.43, 71.38), (31.85, 71.00), (30.95, 70.98),
    (30.52, 70.85), (29.60, 70.50), (28.95, 70.36), (28.42, 69.71), (27.95, 69.20),
    (27.69, 68.85), (27.00, 68.35), (26.20, 68.20), (25.43, 68.31), (24.75, 67.95),
    (24.00, 67.45),
]

# Major barrages / dams on the Indus: name -> (lat, lon)
BARRAGES = {
    "Tarbela Dam": (34.0894, 72.6980),
    "Jinnah (Kalabagh) Barrage": (32.9650, 71.5450),
    "Chashma Barrage": (32.4380, 71.3800),
    "Taunsa Barrage": (30.5250, 70.8500),
    "Guddu Barrage": (28.4250, 69.7110),
    "Sukkur Barrage": (27.6830, 68.8450),
    "Kotri Barrage": (25.4300, 68.3100),
}
