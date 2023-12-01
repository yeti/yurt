import { useRouteError } from 'react-router-dom';
import { IS_DEV } from '~/shared/constants';

//TODO implement error page
export default function ErrorPage() {
  const error = useRouteError();

  IS_DEV && console.error('Error caught at boundary:', error);

  return (
    <div id="error-page">
      <h1>Oops!</h1>
      <p>Sorry, an unexpected error has occurred.</p>
      <p>{error instanceof Error ? error.name : 'Unknown error'} </p>
    </div>
  );
}
