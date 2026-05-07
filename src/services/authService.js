// Simple in-memory storage for users (in production, use a real database)
const users = new Map();

export const authService = {
  // Register a new user
  async register(email, password) {
    // Validate email format (must be @cp.co.id)
    if (!email.endsWith("@cp.co.id")) {
      throw new Error("Email must be a @cp.co.id address");
    }

    // Check if user already exists
    if (users.has(email)) {
      throw new Error("User already registered with this email");
    }

    // Store user (hashed password would be better in production)
    users.set(email, {
      password,
      verified: false,
      verificationCode: generateVerificationCode(),
      createdAt: new Date(),
    });

    return {
      success: true,
      message: "Registration successful",
      verificationCode: users.get(email).verificationCode,
    };
  },

  // Login user
  async login(email, password) {
    // Validate email format
    if (!email.endsWith("@cp.co.id")) {
      throw new Error("Invalid email format. Must be @cp.co.id");
    }

    // Check if user exists
    const user = users.get(email);
    if (!user) {
      throw new Error("User not found. Please register first");
    }

    // Verify password
    if (user.password !== password) {
      throw new Error("Invalid password");
    }

    // Check if email is verified
    if (!user.verified) {
      throw new Error("Please verify your email before logging in");
    }

    // Login successful
    localStorage.setItem(
      "user",
      JSON.stringify({
        email,
        loginTime: new Date().toISOString(),
      }),
    );

    return {
      success: true,
      message: "Login successful",
      user: { email },
    };
  },

  // Verify email with code
  async verifyEmail(email, code) {
    const user = users.get(email);
    if (!user) {
      throw new Error("User not found");
    }

    if (user.verificationCode !== code) {
      throw new Error("Invalid verification code");
    }

    user.verified = true;
    return {
      success: true,
      message: "Email verified successfully",
    };
  },

  // Get current logged-in user
  getCurrentUser() {
    const userJson = localStorage.getItem("user");
    return userJson ? JSON.parse(userJson) : null;
  },

  // Logout
  logout() {
    localStorage.removeItem("user");
    return { success: true, message: "Logged out successfully" };
  },
};

// Helper function to generate a 6-digit verification code
function generateVerificationCode() {
  return Math.floor(100000 + Math.random() * 900000).toString();
}
