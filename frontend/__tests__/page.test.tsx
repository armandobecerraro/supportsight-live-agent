import { render, screen } from '@testing-library/react';
import Page from '@/app/page';

describe('Home Page', () => {
  it('renders the main heading', () => {
    render(<Page />);
    const heading = screen.getByText(/SupportSight Live/i);
    expect(heading).toBeInTheDocument();
  });

  it('contains the start recording button', () => {
    render(<Page />);
    const button = screen.getByRole('button', { name: /Start Recording/i });
    expect(button).toBeInTheDocument();
  });
});
