const { JSDOM } = require('jsdom');
const dom = new JSDOM('<!DOCTYPE html><html><body><div id="content"></div></body></html>');

global.window = dom.window;
global.document = dom.window.document;
const fs = require('fs');
const path = require('path');

describe('Formatting', () => {
    
    beforeEach(() => {
        document.body.innerHTML = fs.readFileSync(path.resolve(__dirname, '../src/index.html'), 'utf-8');
        global.content = document.getElementById("content");
        global.loadButton = document.getElementById("load-button");
        global.executeCommand = require('../src/script.js')
        
    });

    const formattingCommands = [
        { command: 'bold', tag: 'strong' },
        { command: 'underline', tag: 'u' },
        { command: 'italic', tag: 'em' },
        { command: 'strikethrough', tag: 'strike' },
        { command: 'justifyLeft', style: 'text-align: left;' },
        { command: 'justifyCenter', style: 'text-align: center;' },
        { command: 'justifyRight', style: 'text-align: right;' },
        { command: 'justifyFull', style: 'text-align: justify;' },
        { command: 'insertUnorderedList', tag: 'ul', listItemTag: 'li' },
        { command: 'insertOrderedList', tag: 'ol', listItemTag: 'li' }
    ];
    
    test.each(formattingCommands)(
        `should apply $command when $command button is pressed`,
        ({ command, tag, style, listItemTag }) => {
            document.body.innerHTML = '<div id="content" contenteditable="true">Test</div>';
            const content = document.getElementById('content');
    
            // Simulate text selection
            const range = document.createRange();
            const selection = window.getSelection();
            range.selectNodeContents(content);
            selection.removeAllRanges();
            selection.addRange(range);
    
            // Mock execCommand behavior for formatting commands
            global.document.execCommand = jest.fn().mockImplementation((cmd) => {
                if (tag) {
                    if (tag === 'ul' || tag === 'ol') {
                        // If it's a list, create the list tag and the list item
                        const listElement = document.createElement(tag);
                        const listItem = document.createElement(listItemTag);
                        listItem.textContent = content.textContent;
                        listElement.appendChild(listItem);
                        content.innerHTML = '';
                        content.appendChild(listElement);
                    } else {
                        // For other tags (bold, underline, etc.), apply the tag as usual
                        const formatTag = document.createElement(tag);
                        formatTag.textContent = content.textContent;
                        content.innerHTML = '';
                        content.appendChild(formatTag);
                    }
                } else if (style) {
                    // For text-align styles
                    content.style.cssText = style;
                } else if (cmd === 'undo') {
                    // Simulate the undo behavior by reverting the content
                    content.innerHTML = 'Undo Text';
                } else if (cmd === 'redo') {
                    // Simulate the redo behavior by restoring the content
                    content.innerHTML = 'Test';
                }
            });
    
            executeCommand(command);
    
            // Check if execCommand was called with the correct command
            expect(global.document.execCommand).toHaveBeenCalledWith(command);
    
            // If it's a list command, check that the content has the correct list structure
            if (tag === 'ul' || tag === 'ol') {
                expect(content.innerHTML).toContain(`<${tag}><${listItemTag}>Test</${listItemTag}></${tag}>`);
            } else if (tag) {
                // Check that other formatting commands apply the correct tag
                expect(content.innerHTML).toContain(`<${tag}>Test</${tag}>`);
            } else if (style) {
                // Check that text-align styles are correctly applied
                expect(content.getAttribute('style')).toBe(style);
            }
        }
    );
});
