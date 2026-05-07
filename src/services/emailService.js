// Email service for sending verification emails
export const emailService = {
  // Send verification email
  async sendVerificationEmail(email, verificationCode) {
    try {
      // In production, you would use a real email service like:
      // - Nodemailer
      // - SendGrid
      // - Firebase Authentication
      // - AWS SES
      // etc.

      console.log(`
        📧 Verification Email Sent to: ${email}
        ────────────────────────────────
        Your verification code is: ${verificationCode}
        
        Please enter this code to verify your email and complete registration.
        This code will expire in 15 minutes.
        ────────────────────────────────
      `);

      // Simulate email sending delay
      await new Promise((resolve) => setTimeout(resolve, 500));

      return {
        success: true,
        message: `Verification email sent to ${email}`,
        verificationCode, // In production, don't return this
      };
    } catch (error) {
      throw new Error(`Failed to send verification email: ${error.message}`);
    }
  },

  // Send login confirmation email (optional)
  async sendLoginConfirmation(email) {
    try {
      console.log(`
        📧 Login Confirmation Email Sent to: ${email}
        ────────────────────────────────
        You have successfully logged in to your account.
        If this wasn't you, please secure your account immediately.
        ────────────────────────────────
      `);

      await new Promise((resolve) => setTimeout(resolve, 300));

      return {
        success: true,
        message: `Login confirmation sent to ${email}`,
      };
    } catch (error) {
      throw new Error(`Failed to send login confirmation: ${error.message}`);
    }
  },
};
