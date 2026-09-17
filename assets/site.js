document.documentElement.classList.add('js');
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#site-navigation');
function setMenu(open) {
  menuButton.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
}
menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    setMenu(false);
    menuButton.focus();
  }
});
navigation.addEventListener('click', event => { if (event.target.closest('a')) setMenu(false); });
// Optional read-only access to the same content shown on this page.
const context = document.modelContext;
if (context?.registerTool) {
  const lifecycle = new AbortController();
  try {
    Promise.resolve(context.registerTool({
      name: 'read_academic_page',
      description: 'Read a slice of the academic profile content currently displayed on this page.',
      inputSchema: {type: 'object', properties: {offset: {type: 'integer', minimum: 0}}, additionalProperties: false},
      annotations: {readOnlyHint: true, untrustedContentHint: true},
      execute(input) {
        if (!input || typeof input !== 'object' || Object.keys(input).some(k => k !== 'offset') || (input.offset !== undefined && (!Number.isInteger(input.offset) || input.offset < 0))) throw new Error('offset must be a nonnegative integer');
        const offset = input.offset ?? 0;
        const content = document.querySelector('main').innerText;
        return {title: document.title, text: content.slice(offset, offset + 6000), nextOffset: offset + 6000 < content.length ? offset + 6000 : null};
      }
    }, {signal: lifecycle.signal})).catch(() => {});
    window.addEventListener('pagehide', () => lifecycle.abort(), {once: true});
  } catch (_) { /* This optional API does not affect the ordinary website. */ }
}
