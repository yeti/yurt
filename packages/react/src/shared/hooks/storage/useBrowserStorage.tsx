import { useSyncExternalStore, useRef } from 'react';
import { IS_DEV } from '../../constants';

type StorageType = 'localStorage' | 'sessionStorage';

const getStorageObject = (type: StorageType) => {
  return type === 'localStorage' ? window.localStorage : window.sessionStorage;
};

export const useBrowserStorage = <T,>(
  key: string,
  initialValue: T,
  storageType: StorageType,
) => {
  const storage = getStorageObject(storageType);
  const cachedValue = useRef<T>(initialValue);

  const getSnapshot = () => {
    try {
      const item = storage.getItem(key);
      const value = item ? JSON.parse(item) : initialValue;

      if (JSON.stringify(cachedValue.current) !== JSON.stringify(value)) {
        cachedValue.current = value;
      }

      return cachedValue.current as T;
    } catch (error) {
      IS_DEV && console.error(error);

      return initialValue;
    }
  };

  const subscribe = (listener: () => void) => {
    const handleStorageChange = (event: StorageEvent) => {
      if (event.key === key) {
        listener();
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  };

  const setValue = (value: T | ((prev: T) => T)) => {
    try {
      const currentValue = cachedValue.current;
      const newValue = value instanceof Function ? value(currentValue) : value;

      storage.setItem(key, JSON.stringify(newValue));
      cachedValue.current = newValue;

      window.dispatchEvent(
        new StorageEvent('storage', {
          key,
          newValue: JSON.stringify(newValue),
        }),
      );
    } catch (error) {
      IS_DEV && console.error(error);
    }
  };

  const value = useSyncExternalStore(subscribe, getSnapshot);

  return [value, setValue] as const;
};
