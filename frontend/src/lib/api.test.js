import { describe, it, expect } from 'vitest';
import { getMatrixData, saveMatrixData } from './api.js';

describe('api — smoke tests', () => {
  it('getMatrixData est une fonction', () => {
    expect(typeof getMatrixData).toBe('function');
  });

  it('saveMatrixData est une fonction', () => {
    expect(typeof saveMatrixData).toBe('function');
  });

  it('getMatrixData retourne une Promise', () => {
    // On intercepte fetch pour ne pas appeler le réseau
    globalThis.fetch = async () => ({
      ok: true,
      json: async () => ({ ranks: [], pillars: [] })
    });
    const result = getMatrixData();
    expect(result).toBeInstanceOf(Promise);
  });
});
