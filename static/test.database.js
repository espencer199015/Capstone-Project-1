client.query('SELECT version()')
  .then(result => {
    console.log('PostgreSQL Version:', result.rows[0].version);
  })
  .catch(error => {
    console.error('Error executing test query:', error);
  });

  client.query('SELECT * FROM users LIMIT 1')
  .then(result => {
    console.log('First user data:', result.rows[0]);
  })
  .catch(error => {
    console.error('Error querying user data:', error);
  });

  fetch('/users')
  .then(response => response.json())
  .then(data => {
    console.log('User data from API:', data);
  })
  .catch(error => {
    console.error('Error fetching user data:', error);
  });