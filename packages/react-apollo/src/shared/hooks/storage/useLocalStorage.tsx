import { LocalStorageKeys } from '~/shared/constants';
import { useBrowserStorage } from './useBrowserStorage';

const useLocalStorage = <T,>(key: string, initialValue: T) => {
  return useBrowserStorage(key, initialValue, 'localStorage');
};

export const useStoredId = () => {
  const [storedId, setStoredId] = useLocalStorage(
    LocalStorageKeys.StoredId,
    null,
  );

  return { storedId, setStoredId } as const;
};
