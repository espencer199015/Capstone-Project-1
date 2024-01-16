// test.database.js

const { Pool } = require('pg');
const fetch = require('node-fetch');

// Initialize your PostgreSQL client
const pool = new Pool(/* your PostgreSQL connection configuration */);
const client = await pool.connect();

// Describe the integration tests
describe('test.database.js', () => {
  // Test PostgreSQL version query
  test('PostgreSQL Version Query', async () => {
    try {
      const result = await client.query('SELECT version()');
      console.log('PostgreSQL Version:', result.rows[0].version);
    } catch (error) {
      console.error('Error executing PostgreSQL version query:', error);
    }
  });

  // Test PostgreSQL user data query
  test('PostgreSQL User Data Query', async () => {
    try {
      const result = await client.query('SELECT * FROM users LIMIT 1');
      console.log('First user data:', result.rows[0]);
    } catch (error) {
      console.error('Error querying PostgreSQL user data:', error);
    }
  });

  // Test API request
  test('API Request', async () => {
    try {
      const response = await fetch('/users');
      const data = await response.json();
      console.log('User data from API:', data);
    } catch (error) {
      console.error('Error fetching user data from API:', error);
    }
  });
});

// Close the PostgreSQL client after tests
afterAll(async () => {
  await client.end();
});