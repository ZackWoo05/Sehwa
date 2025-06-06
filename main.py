import React, { useEffect, useState } from "react";
import { Map, MapMarker } from "react-kakao-maps-sdk";

const dummyChargers = [
  {
    id: 1,
    name: "서울시청 충전소",
    lat: 37.5665,
    lng: 126.9780,
    status: "충전 가능 ⚡️",
    price: "300원/kWh",
    idleFee: "점거비용 있음 💸",
    freeParking: "무료 주차 가능 🅿️"
  },
  {
    id: 2,
    name: "을지로입구 충전소",
    lat: 37.5660,
    lng: 126.982,
    status: "충전 중 🔌",
    price: "250원/kWh",
    idleFee: "점거비용 없음 ✅",
    freeParking: "무료 주차 불가 ❌"
  }
];

export default function EVChargerMap() {
  const [location, setLocation] = useState({ lat: 0, lng: 0 });
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLocation({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude
        });
        setLoaded(true);
      },
      (err) => {
        alert("위치 정보를 불러올 수 없습니다.");
        setLoaded(true);
      }
    );
  }, []);

  return (
    <div className="w-full h-screen">
      {loaded && (
        <Map
          center={location}
          style={{ width: "100%", height: "100%" }}
          level={4}
        >
          <MapMarker
            position={location}
            image={{
              src: "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png",
              size: { width: 24, height: 35 }
            }}
          />

          {dummyChargers.map((charger) => (
            <MapMarker
              key={charger.id}
              position={{ lat: charger.lat, lng: charger.lng }}
              title={charger.name}
            >
              <div className="p-2 bg-white rounded-xl shadow-xl w-48 text-sm leading-relaxed">
                <strong>{charger.name} 📍</strong><br />
                {charger.status}<br />
                🔋 {charger.price}<br />
                🚫 {charger.idleFee}<br />
                🅿️ {charger.freeParking}
              </div>
            </MapMarker>
          ))}
        </Map>
      )}
    </div>
  );
}
