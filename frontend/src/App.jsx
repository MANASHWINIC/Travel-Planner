import { useState } from "react";
import axios from "axios";

function App() {

  const [form, setForm] = useState({
  source: "",
  destination: "",
  budget: "",
  travelers: "",
  days: "",
  travelDate: "",
  preferences: "",
});

  const [tripPlan, setTripPlan] = useState("");
  const [loading, setLoading] = useState(false);
  const [bookingLinks, setBookingLinks] = useState(null);
  const [flights, setFlights] = useState([]);
  const [recommendedFlight, setRecommendedFlight] = useState(null);
  const [trains, setTrains] = useState([]);
  const [recommendedTrain, setRecommendedTrain] = useState(null);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const generateTrip = async () => {
    if (form.source === form.destination) {
  alert("Source and Destination cannot be the same");
  return;
}
    try {
      if (
  !form.source ||
  !form.destination ||
  !form.travelDate
) {
  alert("Please fill source, destination and travel date");
  return;
}

      setLoading(true);

      const response = await axios.post(
  "http://127.0.0.1:8000/generate-trip",
  {
    source: form.source,
    destination: form.destination,
    budget: Number(form.budget),
    travelers: Number(form.travelers),
    days: Number(form.days),
    travelDate: form.travelDate,
    preferences: form.preferences,
  }
);

      setTripPlan(response.data.trip_plan);

      setBookingLinks(
        response.data.booking_links
      );
      setFlights(
  response.data.flight_data || []
);
setRecommendedFlight(
  response.data.recommended_flight
);
setTrains(
  response.data.train_data || []
);
if (
  response.data.train_data &&
  response.data.train_data.length > 0
) {
  setRecommendedTrain(
    response.data.train_data[0]
  );
} else {
  setRecommendedTrain(null);
}

    } catch (error) {

      console.error(error);
      alert("Failed to generate trip");

    } finally {

      setLoading(false);

    }
  };
console.log("Flights:", flights);
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

      <select
  name="source"
  onChange={handleChange}
  style={inputStyle}
>
  <option value="">Select Source</option>
  <option>Chennai</option>
  <option>Delhi</option>
  <option>Mumbai</option>
  <option>Bangalore</option>
  <option>Hyderabad</option>
  <option>Coimbatore</option>
  <option>Goa</option>
  <option>Kochi</option>
<option>Pune</option>
<option>Kolkata</option>
<option>Ahmedabad</option>
</select>

      <select
  name="destination"
  onChange={handleChange}
  style={inputStyle}
>
  <option value="">Select Destination</option>
  <option>Chennai</option>
  <option>Delhi</option>
  <option>Mumbai</option>
  <option>Bangalore</option>
  <option>Hyderabad</option>
  <option>Coimbatore</option>
  <option>Goa</option>
  <option>Kochi</option>
<option>Pune</option>
<option>Kolkata</option>
<option>Ahmedabad</option>
</select>

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
  type="date"
  name="travelDate"
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
       {recommendedFlight !== null && (
        
  <div
    style={{
      background: "#d4edda",
      padding: "15px",
      borderRadius: "10px",
      marginTop: "20px"
    }}
  >
    <h2>🏆 Recommended Flight</h2>
<p><strong>Airline:</strong> {recommendedFlight.airline}</p>

<p><strong>Price:</strong> ₹{recommendedFlight.price}</p>

<p>
  <strong>Duration:</strong>
  {" "}
  {Math.floor(recommendedFlight.duration / 60)}h
  {" "}
  {recommendedFlight.duration % 60}m
</p>

<p>
  <strong>Platform:</strong>
  {" "}
  {recommendedFlight.gate}
</p>

<p>
  <strong>Departure:</strong>
  {" "}
  {new Date(
    recommendedFlight.departure
  ).toLocaleString()}
</p>

<a
  href={recommendedFlight.booking_url}
  target="_blank"
  rel="noreferrer"
  style={{
    background: "green",
    color: "white",
    padding: "10px 15px",
    borderRadius: "5px",
    textDecoration: "none",
    display: "inline-block",
    marginTop: "10px"
  }}
>
  Book Recommended Flight
</a>
    
  </div>
)}
{recommendedTrain && (
  <div
    style={{
      background: "#fff3cd",
      padding: "15px",
      borderRadius: "10px",
      marginTop: "20px"
    }}
  >
    <h2>🚆 Recommended Train</h2>

    <p><strong>Train:</strong> {recommendedTrain?.train_name}</p>

<p><strong>Number:</strong> {recommendedTrain?.train_number}</p>

<p><strong>Duration:</strong> {recommendedTrain?.duration}</p>

<p><strong>Departure:</strong> {recommendedTrain?.from_std}</p>

<p><strong>Arrival:</strong> {recommendedTrain?.to_std}</p>
  </div>
)}
      {flights.length > 0 && (
  <div
    style={{
      marginTop: "30px",
      padding: "20px",
      border: "1px solid #ddd",
      borderRadius: "10px",
      backgroundColor: "#eef7ff",
    }}
  >
    <h2>✈ Real Flight Prices</h2>

    <table
      style={{
        width: "100%",
        borderCollapse: "collapse",
      }}
    >
      <thead>
        <tr>
  <th style={tableStyle}>Airline</th>
  <th style={tableStyle}>Price</th>
  <th style={tableStyle}>Duration</th>
  <th style={tableStyle}>Departure</th>
  <th style={tableStyle}>Platform</th>
  <th style={tableStyle}>Book</th>
</tr>
      </thead>

      <tbody>
        {flights.map((flight, index) => (
          <tr key={index}>
            <td style={tableStyle}>
              {flight.airline}
            </td>

            <td style={tableStyle}>
              ₹{flight.price}
            </td>

            <td style={tableStyle}>
              {Math.floor(flight.duration / 60)}h {flight.duration % 60}m
            </td>

            <td style={tableStyle}>
              {new Date(
  flight.departure
).toLocaleString()}
            </td>
            <td style={tableStyle}>
  {flight.gate}
</td>
            <td style={tableStyle}>
  <a
    href={flight.booking_url}
    target="_blank"
    rel="noreferrer"
    style={{
      background: "#007bff",
      color: "white",
      padding: "8px 12px",
      borderRadius: "5px",
      textDecoration: "none",
      display: "inline-block"
    }}
  >
    Book
  </a>
</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)
}
{!loading &&
 flights.length === 0 &&
 tripPlan && (
  <div
    style={{
      color: "red",
      marginTop: "20px"
    }}
  >
    No flights found for the selected route/date.
  </div>
)}
     {trains.length > 0 && (
  <div
    style={{
      marginTop: "30px",
      padding: "20px",
      border: "1px solid #ddd",
      borderRadius: "10px",
      backgroundColor: "#fff3cd",
    }}
  >
    <h2>🚆 Available Trains</h2>

    <table
      style={{
        width: "100%",
        borderCollapse: "collapse",
      }}
    >
      <thead>
        <tr>
          <th style={tableStyle}>Train No</th>
          <th style={tableStyle}>Train Name</th>
          <th style={tableStyle}>Departure</th>
          <th style={tableStyle}>Arrival</th>
          <th style={tableStyle}>Duration</th>
          <th style={tableStyle}>Type</th>
          <th style={tableStyle}>Classes</th>
        </tr>
      </thead>

      <tbody>
        {Array.isArray(trains) &&
 trains.map((train, index) => (
          <tr key={index}>
            <td style={tableStyle}>
              {train.train_number}
            </td>

            <td style={tableStyle}>
              {train.train_name}
            </td>

            <td style={tableStyle}>
  {train.from_std}
</td>

<td style={tableStyle}>
  {train.to_std}
</td>

            <td style={tableStyle}>
              {train.duration}
            </td>

            <td style={tableStyle}>
              {train.train_type}
            </td>

            <td style={tableStyle}>
  {Array.isArray(train.class_type)
    ? train.class_type.join(", ")
    : ""}
</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)}
{!loading &&
 trains.length === 0 &&
 tripPlan && (
  <div
    style={{
      color: "orange",
      marginTop: "20px"
    }}
  >
    No trains found for selected route/date.
  </div>
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
const tableStyle = {
  border: "1px solid #ccc",
  padding: "10px",
  textAlign: "left",
};
export default App;