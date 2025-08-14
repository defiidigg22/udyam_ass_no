import { render, screen } from '@testing-library/react';
import UdyamForm from './UdyamForm';

// The 'test' function defines a single test case.
// It takes a description and a function with the test logic.
test('renders the Udyam registration form and its fields', () => {
  // 1. Render the component you want to test into a virtual screen.
  render(<UdyamForm />);
  
  // 2. Find elements on the virtual screen. We'll look for the main heading.
  // We use a regular expression /.../i to make the text match case-insensitive.
  const headingElement = screen.getByText(/Udyam Registration Form/i);
  
  // We can also find an input field by its associated label text.
  const aadhaarInputElement = screen.getByLabelText(/Aadhaar Number/i);

  // 3. Assert that the elements we found are actually in the document.
  // If they are, the test passes. If not, it fails.
  expect(headingElement).toBeInTheDocument();
  expect(aadhaarInputElement).toBeInTheDocument();
});