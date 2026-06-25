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
  const [flights, setFlights] = useState([]);
  const [recommendedFlight, setRecommendedFlight] = useState(null);
  const [trains, setTrains] = useState([]);
  const [recommendedTrain, setRecommendedTrain] = useState(null);
  const [hotels, setHotels] = useState([]);
  const [recommendedHotel, setRecommendedHotel] = useState(null);
  const [tripData, setTripData] = useState(null);

const [feedback, setFeedback] = useState("");

const [showFeedback, setShowFeedback] = useState(false);

const [executionResult, setExecutionResult] = useState(null);

const [approved, setApproved] = useState(false);
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
      setTripData(response.data.trip_data);

      setFlights(
  response.data.flight_data || []
);
setRecommendedFlight(
  response.data.recommended_flight
);
setTrains(
  response.data.train_data || []
);
setRecommendedTrain(
  response.data.recommended_train
) 
setHotels(
  response.data.hotel_data || []
);
setRecommendedHotel(
  response.data.recommended_hotel
);


    } catch (error) {

      console.error(error);
      alert("Failed to generate trip");

    } finally {

      setLoading(false);

    }
  };

console.log("Flights:", flights);
const approveTrip = async () => {

  try {

    const response = await axios.post(

      "http://127.0.0.1:8000/approve-trip",

      {

        trip_data: tripData

      }

    );

    setExecutionResult(response.data);

    setApproved(true);

  }

  catch(err){

    console.log(err);

    alert("Execution Failed");

  }

}
const replanTrip = async () => {

  try{

    const response = await axios.post(

      "http://127.0.0.1:8000/replan-trip",

      {

        trip_data: tripData,

        feedback: feedback

      }

    );

    setTripPlan(

      response.data.trip_plan

    );

    setTripData(

      response.data.trip_data

    );

    setShowFeedback(false);

  }

  catch(err){

    console.log(err);

    alert("Replanning Failed");

  }

}
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
  type="number"
  name="budget"
  placeholder="Budget"
  onChange={handleChange}
  style={inputStyle}
/>

<input
  type="number"
  name="travelers"
  placeholder="Travelers"
  onChange={handleChange}
  style={inputStyle}
/>


<input
  type="number"
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
      background: "#070707",
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
      background: "#000000",
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
      backgroundColor: "#000000",
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
      backgroundColor: "#000000",
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
{recommendedHotel && (
  <div
    style={{
      background: "#0c0c0c",
      padding: "15px",
      borderRadius: "10px",
      marginTop: "20px"
    }}
  >
    <h2>🏨 Recommended Hotel</h2>

    <p>
      <strong>Name:</strong>
      {" "}
      {recommendedHotel.name}
    </p>

    <p>
      <strong>Rating:</strong>
      {" "}
      {recommendedHotel.rating}
    </p>

    <p>
      <strong>Price:</strong>
      {" "}
      ₹{Math.round(
        recommendedHotel.price
      )}
    </p>

    <p>
      <strong>Address:</strong>
      {" "}
      {recommendedHotel.address}
    </p>

    <a
      href={recommendedHotel.booking_url}
      target="_blank"
      rel="noreferrer"
    >
      Book Hotel
    </a>
  </div>
)}
{hotels.length > 0 && (
  <div
    style={{
      marginTop: "30px",
      padding: "20px",
      border: "1px solid #ffffff",
      borderRadius: "10px"
    }}
  >
    <h2>🏨 Hotels</h2>

    {hotels.map((hotel, index) => (
      <div
        key={index}
        style={{
          marginBottom: "20px",
          padding: "15px",
          border: "1px solid #ccc",
          borderRadius: "8px"
        }}
      >
        <h3>{hotel.name}</h3>

        <p>⭐ Rating: {hotel.rating}</p>

        <p>📍 {hotel.address}</p>

        <p>💰 ₹{Math.round(hotel.price)}</p>

        <a
          href={hotel.booking_url}
          target="_blank"
          rel="noreferrer"
        >
          Booking.com
        </a>

        {" | "}

        <a
          href={hotel.agoda_url}
          target="_blank"
          rel="noreferrer"
        >
          Agoda
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
            backgroundColor: "#000000",
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
      {tripPlan && !approved && (

<div
style={{
marginTop:20
}}
>

<button

onClick={approveTrip}

style={{

padding:"12px",

background:"green",

color:"white",

marginRight:"20px",

cursor:"pointer"

}}

>

Approve Trip

</button>

<button

onClick={()=>setShowFeedback(true)}

style={{

padding:"12px",

background:"orange",

color:"white",

cursor:"pointer"

}}

>

Replan Trip

</button>

</div>

)}
{showFeedback && (

<div
style={{
marginTop:20
}}
>

<textarea

rows={5}

style={{
width:"100%"
}}

placeholder="Tell the AI what should change"

value={feedback}

onChange={(e)=>

setFeedback(e.target.value)

}

/>

<button

onClick={replanTrip}

style={{

marginTop:10,

padding:10

}}

>

Submit Feedback

</button>

</div>

)}
{executionResult && (

<div

style={{

marginTop:30,

padding:20,

border:"1px solid green",

borderRadius:10

}}

>

<h2>

Execution Agent Completed

</h2>

<p>

📅 Calendar

{executionResult.calendar_status}

</p>

<p>

📱 WhatsApp

{executionResult.whatsapp_status}

</p>

<p>

📄 PDF Generated

</p>

<a

href="http://127.0.0.1:8000/download-pdf"

target="_blank"

>

Download PDF

</a>

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