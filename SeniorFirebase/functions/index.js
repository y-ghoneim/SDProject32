const functions = require("firebase-functions");
const admin = require("firebase-admin");
admin.initializeApp();

exports.addHealthData = functions.https.onRequest(async (req, res) => {
  // Check for POST request
  if (req.method !== "POST") {
    return res.status(405).send("Method Not Allowed");
  }

  // Get u_id from headers
  const uid = req.headers["uid"];
  if (!uid) {
    return res.status(401).send("Unauthorized: No uid provided.");
  }

  try {
    // Check if the user exists in the 'users' collection
    const userDoc = await admin.firestore().collection("users").doc(uid).get();

    if (!userDoc.exists) {
      return res.status(401).send("Unauthorized: u_id does not exist.");
    }

    // User exists, now add the health data to 'TestCollection'
    const healthData = req.body;
    // Add any necessary processing or validation for healthData here
    const writeResult = await admin.firestore().collection("TestCollection").add(healthData);
    return res.status(201).send(`Patient data added with ID: ${writeResult.id}`);
  } catch (error) {
    console.error("Error processing request", error);
    return res.status(500).send("Internal Server Error");
  }
});
