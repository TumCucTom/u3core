/* web server for hosting web app and making RESTful calls */
/* eslint-disable no-console */
/* eslint-disable no-unused-vars */

const mysql = require('mysql2');
const bcrypt = require('bcrypt');
const cors = require('cors');
const express = require('express');
const nodemailer = require('nodemailer');
const crypto = require('crypto');

const app = express();

const corsOptions = {
  origin: 'http://localhost:9000',
  methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
  credentials: true,
};

app.use(cors(corsOptions));
app.use(express.json());

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'trvbale',
  password: 'MLAI01',
  database: 'MLAIDB',
});

connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL:', err);
    return;
  }
  console.log('Connected to MySQL server');
});

app.get('/api/emails', (req, res) => {
  const query = 'SELECT email FROM customerLogins';
  connection.query(query, (error, results) => {
    if (error) {
      console.error('Error fetching emails:', error);
      res.status(500).json({ error: 'Internal Server Error' });
      return;
    }
    const emails = results.map((result) => result.email);
    res.json(emails);
  });
});

app.get('/api/login', (req, res) => {
  const emailLogin = req.query.emailVar;
  const query3 = 'SELECT encyrptedPassword FROM customerLogins WHERE email = ?';
  connection.query(query3, [emailLogin], (error, results) => {
    if (error) {
      console.error('Error fetching data:', error);
      res.status(500).json({ error: 'Internal Server Error' });
      return;
    }
    if (results.length === 0) {
      res.json(null);
    } else {
      const hashedPassword = results[0].encryptedPassword;
      res.json(hashedPassword);
    }
  });
});

app.post('/api/addToCustomer', async (req, res) => {
  const fName = req.body.items[0];
  const lName = req.body.items[1];
  const email = req.body.items[2];
  const password = req.body.items[3];

  // Hash the password
  const hashedPassword = await bcrypt.hash(password, 10);

  console.log('Original Password:', password);
  console.log('Hashed Password:', hashedPassword);

  const query = 'INSERT INTO Customer (firstname, lastname) VALUES (?, ?)';
  connection.query(query, [fName, lName], (error, results) => {
    if (error) {
      console.error('Error adding item to customer:', error);
      res.status(500).json({ message: 'Internal Server Error' });
      return;
    }
    const customerID = results.insertId;

    const query2 = 'INSERT INTO CustLogin (email, hashPWord, customerID) VALUES (?,?,?)';
    connection.query(query2, [email, hashedPassword, customerID], (error2, resultVarIgnored) => {
      if (error2) {
        console.error('Error adding item to customerLogin:', error);
        res.status(500).json({ message: 'Internal Server Error' });
      } else {
        res.json({ message: 'Item added successfully to CustomerLogin' });
      }
    });
  });
});

app.post('/api/sendResetEmail', (req, res) => {
  console.log('sendEmail endpoint hit with data:', req.body);
  const { email } = req.body;

  // First, check if the email exists in the database
  const query = 'SELECT email FROM CustomerLogins WHERE email = ?';
  connection.query(query, [email], (error, results) => {
    if (error) {
      console.error('Error querying the database:', error);
      return res.status(500).json({ message: 'Internal Server Error', error: error.toString() });
    }

    // If email does not exist, respond with an error
    if (results.length === 0) {
      return res.status(404).json({ message: 'Email not found' });
    }

    // Proceed with sending the email if the email is found
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: 'u3Core@gmail.com',
        pass: 'auftest123',
      },
    });

    // Generate a secure random token
    const verificationToken = crypto.randomBytes(20).toString('hex');
    const verificationLink = `http://localhost:9000/#/ResetPassword?token=${verificationToken}&email=${encodeURIComponent(email)}`;

    const mailOptions = {
      from: 'u3Core@gmail.com',
      to: email,
      subject: 'Password Reset Request',
      html: `
    <div style="border: 1px solid #f04c26; background-color: #ffffff; padding: 40px; max-width: 800px; margin: auto; font-family: Arial, sans-serif; box-shadow: 0 8px 10px rgba(0, 0, 0, 0.15); text-align: center;">
      <p style="font-size: 16px; font-weight: bold;">This is a password reset request email. Clicking the button below will redirect you to a new page where you can verify your email and reset your password:</p>
      <div style="margin: 40px auto;"> 
        <a href="${verificationLink}" target="_blank" style="background: linear-gradient(to right, #0e004d, #064e81); color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: block; max-width: 250px; width: 80%; margin: auto; font-size: 16px; font-weight: bold;">Verify and Reset Password</a>
      </div>
    </div>
  `,
    };

    transporter.sendMail(mailOptions, (mailError, info) => {
      if (mailError) {
        console.log(mailError);
        console.error('Error sending email:', mailError);
        return res.status(500).send({ message: 'Error sending email', error: mailError.toString() });
      }
      console.log(`Email sent: ${info.response}`);
      return res.status(200).send({ message: 'Email sent successfully', info: info.response });
    });
    return res.status(404).json({ message: 'Unidentified internal error' });
  });
});

app.post('/api/sendVerifyEmail', (req, res) => {
  console.log('sendEmail endpoint hit with data:', req.body);
  const { email } = req.body;

  // First, check if the email exists in the database
  const query = 'SELECT email FROM CustomerLogins WHERE email = ?';
  connection.query(query, [email], (error, results) => {
    if (error) {
      console.error('Error querying the database:', error);
      return res.status(500).json({ message: 'Internal Server Error', error: error.toString() });
    }

    // If email does not exist, respond with an error
    if (results.length === 0) {
      return res.status(404).json({ message: 'Email not found' });
    }

    // Proceed with sending the email if the email is found
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: 'u3Core@gmail.com',
        pass: 'auftest123',
      },
    });

    // Generate a secure random token
    const verificationToken = crypto.randomBytes(20).toString('hex');
    const verificationLink = `http://localhost:9000/#/VerifiedPassword?token=${verificationToken}&email=${encodeURIComponent(email)}`;
    const code = Math.random() * 1000;

    const mailOptions = {
      from: 'u3core@gmail.com',
      to: email,
      subject: 'Email verification',
      html: `
    <div style="border: 1px solid #f04c26; background-color: #ffffff; padding: 40px; max-width: 800px; margin: auto; font-family: Arial, sans-serif; box-shadow: 0 8px 10px rgba(0, 0, 0, 0.15); text-align: center;">
      <p style="font-size: 16px; font-weight: bold;">This is a verification email. Clicking the button below will redirect you to a new page where you can verify your email. Alternatively, you can enter the code below into the OTP page you just left.</p>
      <div style="margin: 40px auto;"> 
        <a href="${verificationLink}" target="_blank" style="background: linear-gradient(to right, #0e004d, #064e81); color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: block; max-width: 250px; width: 80%; margin: auto; font-size: 16px; font-weight: bold;">Verify and Reset Password</a>
      </div>
      <div style="margin-top: 40px; width: 100%; display: flex; justify-content: center;">
        <p style="font-size: 50px;">String(code)</p>
      </div>
    </div>
  `,
    };

    transporter.sendMail(mailOptions, (mailError, info) => {
      if (mailError) {
        console.log(mailError);
        console.error('Error sending email:', mailError);
        return res.status(500).send({ message: 'Error sending email', error: mailError.toString() });
      }
      console.log(`Email sent: ${info.response}`);
      return res.status(200).send({ message: 'Email sent successfully', info: info.response });
    });
    return res.status(404).json({ message: 'Unidentified internal error' });
  });
});
