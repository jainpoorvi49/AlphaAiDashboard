"use client"

import React, { useState } from "react";
import styles from './addUser.module.css';

const AddUser = () => {
  // State to store the form data
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [mobile, setMobile] = useState('');
  const [broker, setBroker] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    const newUserData = {
      user_id: userId,
      password: password,
      mobile_number: mobile,
      broker_name: broker,
    };

    try {
      // Retrieve token from localStorage
      const token = localStorage.getItem("access_token");

      const response = await fetch('http://localhost:8000/user/add/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(newUserData),
      });

      if (!response.ok) {
        throw new Error('Failed to add user');
      }

      const result = await response.json();
      setSuccess('User added successfully!');
      // Reset form fields after successful submission
      setUserId('');
      setPassword('');
      setMobile('');
      setBroker('');
    } catch (error) {
      setError('Error: ' + error.message);
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>Add User</h1>

      {/* Display success or error messages */}
      {error && <div className={styles.error}>{error}</div>}
      {success && <div className={styles.success}>{success}</div>}

      <form className={styles.form} onSubmit={handleSubmit}>
        <div className={styles.formGroup}>
          <label htmlFor="userId">User ID</label>
          <input
            type="text"
            id="userId"
            placeholder="Enter User ID"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            placeholder="Enter Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="mobile">Mobile Number</label>
          <input
            type="text"
            id="mobile"
            placeholder="Enter Mobile Number"
            value={mobile}
            onChange={(e) => setMobile(e.target.value)}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="broker">Broker Name</label>
          <input
            type="text"
            id="broker"
            placeholder="Enter Broker Name"
            value={broker}
            onChange={(e) => setBroker(e.target.value)}
          />
        </div>
        <button type="submit" className={styles.submitButton}>
          Submit
        </button>
      </form>
    </div>
  );
};

export default AddUser;
