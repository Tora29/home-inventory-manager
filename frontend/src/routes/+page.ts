import { load as fetchItems } from "$shared/api/fetchItems"
import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
  const items = await fetchItems(0, 25)
  return { items }
};
