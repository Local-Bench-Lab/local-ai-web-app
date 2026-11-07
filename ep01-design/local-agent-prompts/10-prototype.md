Task 10 of 11 for "Bench Board": connect the prototype. Use list_layers and get_node to find ids. Use proto.interaction.add for every link and proto.flow.add for the flows.

1. Flows: "Desktop" starting at "Home – start"; "Mobile" starting at "Home – mobile".
2. Load animation: on "Home – start", trigger afterDelay 300 ms → navigate to "Home", transition smartAnimate, 700 ms, easeOut.
3. Nav: in the Nav component's variants Page=Home, Page=Leaderboard and Page=Request, give each "link/Home", "link/Leaderboard", "link/Request a test" frame an onClick → navigate to the matching page ("Home", "Leaderboard", "Request"), dissolve, 200 ms.
4. The Button instance in Home's hero: onClick → navigate to "Leaderboard", smartAnimate, 400 ms.
5. Race: on the Race component variant State=Start, afterDelay 400 ms → changeTo the State=Grown variant, smartAnimate, 1200 ms, easeOut. On the "Leaderboard" frame, afterDelay 2200 ms → navigate to "Leaderboard – ranked", smartAnimate, 800 ms, easing bouncy.
6. Details: in the Race variant State=Ranked, the row "row/LFM2.5 24B": onClick → openOverlay "LFM details" (action params position "center", close_on_outside true), smartAnimate, 300 ms.
7. Form: the "send" button on "Request": onClick → navigate to "Request – error", instant. The "send" button on "Request – error": onClick → navigate "Request – sending", dissolve 200 ms. On the "Request – sending" frame: afterDelay 1200 ms → navigate "Request – done", smartAnimate 500 ms.
8. Mobile: the "hamburger" in "Home – mobile"'s Nav instance: onClick → navigate "Menu open", transition moveIn (direction left), 250 ms. In "Menu open"'s Drawer instance: "close" onClick → back (no dest), dissolve 200 ms; "drawer/Leaderboard" onClick → navigate "Leaderboard", 250 ms.
