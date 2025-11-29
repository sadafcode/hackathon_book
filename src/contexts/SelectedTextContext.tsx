import React, { createContext, useState, useEffect, useContext, ReactNode } from 'react';

interface SelectedTextContextType {
  selectedText: string;
  setSelectedText: (text: string) => void;
  clearSelectedText: () => void;
}

const SelectedTextContext = createContext<SelectedTextContextType | undefined>(undefined);

export const SelectedTextProvider = ({ children }: { children: ReactNode }) => {
  const [selectedText, setSelectedTextState] = useState<string>('');

  const clearSelectedText = () => {
    setSelectedTextState('');
  };

  const setSelectedText = (text: string) => {
    // Only update if the text is different to avoid unnecessary re-renders
    if (text !== selectedText) {
      setSelectedTextState(text);
    }
  };

  useEffect(() => {
    const handleSelectionChange = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().length > 0) {
        // Debounce or filter short selections if needed
        setSelectedText(selection.toString());
      } else {
        clearSelectedText();
      }
    };

    document.addEventListener('mouseup', handleSelectionChange);
    // Consider 'selectionchange' for more immediate updates, but 'mouseup' is often sufficient
    // document.addEventListener('selectionchange', handleSelectionChange);

    return () => {
      document.removeEventListener('mouseup', handleSelectionChange);
      // document.removeEventListener('selectionchange', handleSelectionChange);
    };
  }, [selectedText]); // Rerun effect if selectedText changes to clear if selection becomes empty

  return (
    <SelectedTextContext.Provider value={{ selectedText, setSelectedText, clearSelectedText }}>
      {children}
    </SelectedTextContext.Provider>
  );
};

export const useSelectedText = () => {
  const context = useContext(SelectedTextContext);
  if (context === undefined) {
    throw new Error('useSelectedText must be used within a SelectedTextProvider');
  }
  return context;
};
