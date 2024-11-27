/* web server for hosting web app and making RESTful calls */
/* eslint-disable no-console */
/* eslint-disable no-unused-vars */

const mysql = require('mysql2');
const bcrypt = require('bcrypt');
const cors = require('cors');
const express = require('express');

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
  user: 'valentinavelasco',
  password: 'Activated01',
  database: 'SocialMediaApp',
});

connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL:', err);
    return;
  }
  console.log('Connected to MySQL server');
});

app.get('/api/emails', (req, res) => {
  const query = 'SELECT email FROM custLogin';
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
  const query3 = 'SELECT hashPWord FROM custLogin WHERE email = ?';
  connection.query(query3, [emailLogin], (error, results) => {
    if (error) {
      console.error('Error fetching data:', error);
      res.status(500).json({ error: 'Internal Server Error' });
      return;
    }
    if (results.length === 0) {
      res.json(null);
    } else {
      const hashedPassword = results[0].hashPWord;
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
