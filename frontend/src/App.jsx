import { useState } from "react";
import axios from "axios";

function App() {

  const [form, setForm] = useState({
    source: "",
    destination: "",
    budget: "",
    travelers: "",
    days: "",
    preferences: "",
  });

  const [tripPlan, setTripPlan] = useState("");
  const [loading, setLoading] = useState(false);
  const [bookingLinks, setBookingLinks] = useState(null);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const generateTrip = async () => {
    try {

      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/generate-trip",
        {
          source: form.source,
          destination: form.destination,
          budget: Number(form.budget),
          travelers: Number(form.travelers),
          days: Number(form.days),
          preferences: form.preferences,
        }
      );

      setTripPlan(response.data.trip_plan);

      setBookingLinks(
        response.data.booking_links
      );

    } catch (error) {

      console.error(error);
      alert("Failed to generate trip");

    } finally {

      setLoading(false);

    }
  };

  return (
    <div
      style={{
        maxWidth: "1000px",
        margin: "auto",
        padding: "30px",
        fontFamily: "Arial",
      }}
    >

      <h1>✈️ AI Travel Planner</h1>

      <input
        name="source"
        placeholder="Source City"
        onChange={handleChange}
        style={inputStyle}
      />

      <input
        name="destination"
        placeholder="Destination"
        onChange={handleChange}
        style={inputStyle}
      />

      <input
        name="budget"
        placeholder="Budget"
        onChange={handleChange}
        style={inputStyle}
      />

      <input
        name="travelers"
        placeholder="Travelers"
        onChange={handleChange}
        style={inputStyle}
      />

      <input
        name="days"
        placeholder="Days"
        onChange={handleChange}
        style={inputStyle}
      />

      <input
        name="preferences"
        placeholder="Beach, Adventure, Food..."
        onChange={handleChange}
        style={inputStyle}
      />

      <button
        onClick={generateTrip}
        style={{
          padding: "12px 20px",
          cursor: "pointer",
          marginTop: "10px",
          borderRadius: "5px",
        }}
      >
        Generate Trip
      </button>

      {loading && (
        <h3 style={{ marginTop: "20px" }}>
          Generating itinerary...
        </h3>
      )}

      {bookingLinks && (
        <div
          style={{
            marginTop: "30px",
            padding: "20px",
            border: "1px solid #ddd",
            borderRadius: "10px",
            backgroundColor: "#f5f5f5",
          }}
        >

          <h2>✈ Flight Booking Platforms</h2>

          {bookingLinks.flights.map((item) => (
            <div key={item.name}>
              <a
                href={item.url}
                target="_blank"
                rel="noreferrer"
              >
                {item.name}
              </a>
            </div>
          ))}

          <br />

          <h2>🏨 Hotel Booking Platforms</h2>

          {bookingLinks.hotels.map((item) => (
            <div key={item.name}>
              <a
                href={item.url}
                target="_blank"
                rel="noreferrer"
              >
                {item.name}
              </a>
            </div>
          ))}

          <br />

          <h2>🎟 Activities & Tours</h2>

          {bookingLinks.activities.map((item) => (
            <div key={item.name}>
              <a
                href={item.url}
                target="_blank"
                rel="noreferrer"
              >
                {item.name}
              </a>
            </div>
          ))}

        </div>
      )}

      {tripPlan && (
        <div
          style={{
            marginTop: "30px",
            padding: "20px",
            border: "1px solid #ddd",
            borderRadius: "10px",
            backgroundColor: "#f9f9f9",
          }}
        >

          <h2>Generated Itinerary</h2>

          <pre
            style={{
              whiteSpace: "pre-wrap",
              lineHeight: "1.6",
            }}
          >
            {tripPlan}
          </pre>

        </div>
      )}

    </div>
  );
}

const inputStyle = {
  width: "100%",
  padding: "12px",
  marginTop: "10px",
  marginBottom: "10px",
  borderRadius: "5px",
  border: "1px solid #ccc",
};

export default App;