title: Go is Fun, Familiar, and FAST
date: 2014-08-19 09:45
categories: go golang adserver

Over the past few months, in my (nonexistent) spare time, I've been playing
around with [Go](http://www.golang.org), the Google backed language created by
some of my programming heroes. At this point, it feels to me like a cross between
a *much* nicer C and a bit stricter (in a good way) Python. After you get past
all the language niceties, the ultimate trade-off versus an interpreted language
like Python is static typing for speed and increased type safety. And that's
something I'm at least willing to explore.

## Not Your Average Pythonista

I should preface this by reminding you that I have 8+ years experience writing
high-frequency trading servers in C++, so I'm no stranger to C-style languages.
I fully understand things like pointers, memory allocation, the implications of
garbage collected languages, and concurrency. Many coming from interpreted
languages are not so lucky, and that might be one of the biggest hurdles in
diving into Go. Particularly pointers, which tends to be the subject that causes
the highest percentage of students to quit Computer Science.

But having such a background gives me perspective as well. When I left the
finance industry, I was using C++14 extensively on the newest releases of gcc
and Clang, so I know both the power and pain of these types of languages. A
couple of things I found amazing about Go, right off the bat:

#### Compilation times are nonexistent

You might hear that a hundred times, but until you actually get into a code, compile, test
cycle you have *no idea* how crazily fast compilation is.

#### Tool support is already better than C/C++. 

Because it's so quick to compile a program, rather than writing your own language parser
(which, granted, would be much easier to do for Go) to mark errors dynamically, in-line, you
can simply compile the program and use the compiler's (fantastic) output to generate
them. This means in VIM I already have "check file on save" functionality that points out
*actual compiler errors* every time I save the file, totally seamlessly. As
recently as last year, **no C++ IDEs had that feature in a usable state.** 

Also, due to the language's strong support for introspection, semantic completers have
already been written. And they work for third-party packages, too. Not just the
standard library. *And* they can do things like automatically add missing
imports and remove unused ones. Again, this is light-years ahead of the state of editors
for C and C++, which usually rely on time-consuming static analysis to get the
information to perform such actions.

## Go is Fun, Friendly, and FAST

Programming in Go is a bit like coming home for me. It feels nice to get much closer to
the metal, though perhaps not quite as close as I was before. I actually *like*
static typing (although I also **really like** generic programming, something
painfully absent from Go), as I feel it makes programs a bit easier to reason
about. Especially when type inference occurs whenever possible, static typing is
not the issue for me that it sometimes is for others.

Go, it must be said, has a great standard library. It's a thoroughly *modern*
language in this regard. Much is geared towards networked applications and one
can get quite far without relying on third-party packages. Of course, when you
eventually need to use an outside package, Go makes it absurdly easy to include
it by supporting git repos as dependencies. Just as easily as one can import the
`log` package, one can import from the `github.com/coreos/etcd` project. Here
are the import statements for both:

    #!go
    import (
        "log"

        "github.com/coreos/etcd/etcd"
    )

Yeah. That's pretty nice. Go is "friendly" in that way. It's also both fun and friendly
that idiomatic code in the language is clear and comprehensible. To demonstrate,
I decided to build an ad server (a wink to my [employer](http://careers.appnexus.com)).
An ad server is just a highly-specialized web server, so we'll get to see a lot
of Go's web-related packages.

After installing Go and getting your environment setup (making sure the
`$GOPATH` variable is correctly set), you can start with the following code:

    #!go
    package main

    import (
        "log"
    )

    func main() {
        log.Println("---Starting adserver---")
        log.Println("---Stopping adserver---")
    }

While not quite a "Hello, World", it's pretty close. You can build this program
by typing `go build`. The binary, which has no dependencies and can be run
anywhere (an awesome feature), should appear in your directory. Running it gives
the following, as expected:

    #!bash
    $ ./adserver
    2014/08/19 10:21:11 ---Starting adserver---
    2014/08/19 10:21:11 ---Stopping adserver---

You'll notice a few things about the program. Imports are Python-esque and
should be familiar. The `package` directive is used to logically group code and
breaks any dependencies on a Java-like file system-based package system. The
uppercase function calls may look odd, but you'll get used to it. 

Interestingly, case serves a similar purpose as the leading underscore in Python: it determines
if a symbol exported or not (that is, usable from other files/packages).
Anything uppercase is exported, including functions, variables, and types. All
names beginning with a lowercase letter are local to that scope. This goes for
*within* a block as well: if you define a type with a `height` field, it's only
usable internally. You'll have to name it `Height` if you want others to be
able to access it.

### Moar Internets

Given this wholly uninteresting starting point, let's add a little support for
actually serving content. Go grab your favorite image and pretend it's an ad.
Save it wherever you'd like. We're going to imagine that the URLs hitting our
server are part of `<img>` tags or JavaScript calls for ad content. So when I
hit `/ad/1`, I'm saying show me the ad with ID 1 (all ads will get a unique ID).

Let's add a `handler` function to determine the ID of the ad to serve and just
print it to the console and page:

    #!go

    package main

    import (
        "log"
        "net/http"
    )

    func adHandler(w http.ResponseWriter, r *http.Request) {
        id := r.URL.Path[len("/ad/"):]
        log.Println(id)
        w.Write([]byte(id))
    }
    func main() {
        log.Println("---Starting adserver---")
        http.HandleFunc("/ad/", adHandler)
        http.ListenAndServe(":8081", nil)
        log.Println("---Stopping adserver---")
    }

We've created `adHandler`, which takes the standard set of parameters for all
handler functions. We get `id` by doing some Python-like slicing of the passed
in URL. If the URL is `/ad/1`, we want everything after `/ad/` (i.e. the `1`).
Notice the `:=` symbol. This is used for assignment *within functions* and
doesn't require us to specify the type; Go's compiler will do that for us.

Next, we print it out to the log. Finally, we send it back as the body of the
HTTP response by calling `w.Write`. Since `id` is a `string` and `w.Write`
expects a `byte` slice, we need to *cast* id to the proper type (`strings` can
be freely casted to a sequence of bytes, for obvious reasons).

The only other lines of code register `adHandler` with the endpoint `/ad/`
(anything that *starts* with `/ad/` will be sent to `adHandler`; it doesn't have
to be an exact match), and start the server (listening on port `8081`). By
pointing your browser to [http://localhost/ad/3](http://localhost/ad/3), you
should see `3` both on the page and in the console.

### Further In*struct*tion

To represent an ad to be shown as the result of an ad call like the one we just
made, it makes sense to create a structure with all of the ad's information
(like height, width, ID, etc). To do so, we define a new type based on a
structure we outline. We can also create new types that are simply aliases for
existing ones, or combinations of existing ones. Here we create an `CreativeId` type
(really just an int) and a `Creative` type (industry jargon
for the actual picture or movie shown to the user):

    #!go
    type CreativeId int

    type Creative struct {
        Id		CreativeId
        Width	int
        Height	int
        Path    string
    }

So any time you see `CreativeId` you can think `int`. Why is that useful? Because
later, we'll be referring to `Id` quite a bit, and just having `int` causes some
confusion: are we talking about the `Id int`, the `Width int`, or the `Height
int`? This makes our meaning more explicit.

The `Creative` `struct` is a *structure* comprised of four fields: `Id`, `Width`,
`Height`, and `Path`. Note their types follow the names and are automatically justified
by Go's `go fmt` tool, another convenience feature of the language. It's
automatically built in to my Vim setup so that when I save a file, it's run
through `go fmt` and the output is what is actually saved. `go fmt` will do all
sorts of little things, and I've come to love it.

One last thing to note: notice the case of the first letter of each field.
They're all uppercase, which means all of these fields will be available to all
code that makes use of the `Creative` type. If we wanted to create fields that
other code had no reason to know about or access, we would name them with a
lowercase leading character.

### Data Structures! Yay!

We'll need to save all of our creatives in some sort of data structure. In
Python, we would probably create a `dict` with a `Creative`'s `Id` as the keys
and the actual `Creative` object as the value. In Go, `dict` is spelled `M-A-P`:

    #!go
    var adMap = make(map[CreativeId] *Creative)

This line is pretty dense, so we'll discuss it one part at a time. First is the
previously unfamiliar `var`. This is used to declare variables outside of a
function, at the top-level scope. It can also be used with an *initializer*,
seen here. Why the difference between `:=` inside functions and `var` outside?
One key reason is all top-level statements begin with a keyword, which is useful
for a number of uninteresting reasons. `a := 3` doesn't begin with a keyword.
`var a = 3` or `var a int` does.

Ignoring the `make` call for a minute, we see we're creating a `map[CreativeId] *Creative`,
or "A `map` with keys of type `CreativeId` and values of type `pointer to a Creative`.
Pointers are beyond the scope of this article, but suffice it to say that every
variable in Go has a certain address (much like a street address) in memory,
indicating where to find it. `var a Creative` creates enough space in memory for an 
entire `Creative` struct (3 integers), while `var a *Creative` stores only the
*address* to a place in memory that a full `Creative` object can be found.

In Go, a `map` must be *initialized* with the `make` function. This is the
process that actually reserves memory for information the `map` needs to store.
This is similar to how pointers work in terms of requiring the initialization of
the memory being pointed to, but is beyond the scope of this article.

Suffice it to say that the end result of the above statement is that we have a
`map` of `CreativeId` -> `Creative`.

### Initializing Data

Now that we have a place to store `Creative`s, let's fill that puppy up! First,
we need a way to create a new `Creative` (you'll notice there was nothing like
an `__init__` function, or a constructor, defined). Initialization functions in
Go get no special treatment and are simply named `New<Typename>` by convention.
Their signature is `func New<Typename>([args...]) *Typename`. That is, a
function that takes zero or more arguments and returns a pointer to the type in
question.

For our `Creative` type, no fancy initialization is necessary. In fact, we can
simply return a *literal* in `NewCreative`. Object literals look like this:

    #!go
    func NewCreative(height, width int, path string) *Creative{
        return &Creative{}
    }

Supplying empty braces (`{}`), will zero-initialize all fields, which in our
case is *almost* fine (aside from ignoring the arguments passed to the function)
. The one field we don't want zero-initialized is the `Id`, which should be
unique between instances. Let's create a way to get a new unique
`Id` every time we create a new `Creative`:

    #!go
    var creativeUniqueId CreativeId = 0

    func uniqueId() CreativeId {
        creativeUniqueId += 1
        return creativeUniqueId
    }

We define a `creativeUniqueId` to hold the current value and define a function
to get the next unique value. We then change our `NewCreative` initialization
function to use this:

    #!go
    func NewCreative(height, width int, path string) *Creative {
        return &Creative{Id: uniqueId(), Height: height, Width: width, Path: path}
    }

You can explicitly name each field in the `struct`, use the order they were
declared in, or a combination thereof.

### Fill 'er Up

Now that we can create a `Creative`, let's add it to the `adMap`:


    #! go
    func registerCreative(c *Creative) {
        adMap[c.Id] = c
    }

A function seems like overkill at the moment, but we'll be making changes
shortly.

Finally, lets create, register, and serve our first `Creative`. Create a
directory called `images` and place an image there. Rename the image `jeff.jpg`,
or replace it below. Here's the full code listing now:

    #!go

    package main

    import (
        "log"
        "net/http"
        "path/filepath"
        "strconv"
    )

    type CreativeId int

    type Creative struct {
        Id     CreativeId
        Width  int
        Height int
        Path   string
    }

    var creativeUniqueId CreativeId = 0

    func uniqueId() CreativeId {
        creativeUniqueId += 1
        return creativeUniqueId
    }

    func NewCreative(height, width int, path string) *Creative {
        return &Creative{Id: uniqueId(), Height: height, Width: width, Path: path}
    }

    func registerCreative(c *Creative) {
        adMap[c.Id] = c
    }

    var adMap = make(map[CreativeId]*Creative)

    func adHandler(w http.ResponseWriter, r *http.Request) {
        id, _ := strconv.Atoi(r.URL.Path[len("/ad/"):])
        creative, _ := adMap[CreativeId(id)]
        http.ServeFile(w, r, filepath.Join("images", creative.Path))
    }
    func main() {
        log.Println("---Starting adserver---")
        n := NewCreative(10, 10, "jeff.jpg")
        registerCreative(n)
        log.Println(n)
        http.HandleFunc("/ad/", adHandler)
        http.ListenAndServe(":8081", nil)
        log.Println("---Stopping adserver---")
    }

Now if I build and start the server, I can navigate to [http://localhost:8081/ad/1](http://localhost:8081/ad/1) and
see our image generated.

### Moar Power

That's pretty good for a start, but what if we wanted to add things like
logging, statistics gathering, and serving creatives based on whether or not
they fit (width and height) into the ad space provided? Here's a slightly more
complex version I wrote, almost all of which should still be familiar to you.
It's broken up into two files:

###### `creative.go`

    #!go
    package creative

    import "time"

    type CreativeId int

    type Creative struct {
        Id            CreativeId
        Height, Width int
        Path          string
    }

    type CreativeStat struct {
        Impressions   int
        LastServed    time.Time
        ServedPerHour map[int]int
    }

    func NewCreativeStat() *CreativeStat {
        return &CreativeStat{0, time.Now(), make(map[int]int, 24)}
    }

    var universalCreativeId CreativeId = 0

    func getId() CreativeId {
        universalCreativeId += 1
        return universalCreativeId
    }

    func NewCreative(path string, width, height int) *Creative {
        return &Creative{Id: getId(), Height: height, Width: width, Path: path}
    }


##### `main.go`

    #!go

    package main

    import (
        "log"
        "net/http"
        "os"
        "path/filepath"
        "strconv"
        "time"

        "github.com/jeffknupp/adserver/creative"
    )

    var staticFilePath = filepath.Join("/srv", "www", "adserver", "static")

    var adMap = make(map[creative.CreativeId]*creative.Creative)
    var heightIndex = make(map[int][]creative.CreativeId)
    var widthIndex = make(map[int][]creative.CreativeId)

    var adStats = make(map[int]*creative.CreativeStat)

    func registerCreative(ad *creative.Creative) {
        adMap[ad.Id] = ad
        heightIndex[ad.Height] = append(heightIndex[ad.Height], ad.Id)
        widthIndex[ad.Width] = append(widthIndex[ad.Width], ad.Id)
    }

    func recordImpression(stat *creative.CreativeStat, ad *creative.Creative) {
        stat.Impressions += 1
        previousServed := stat.LastServed
        stat.LastServed = time.Now()
        stat.ServedPerHour[time.Now().Hour()] += 1
        log.Printf("Serving ad[%d]\n", ad.Id)
        log.Printf("Total Impressions: [%d]\n", stat.Impressions)
        log.Printf("Previously served at: [%s]\n", previousServed.UTC())
        log.Printf("Served this hour: [%d]\n", stat.ServedPerHour[time.Now().Hour()])
    }

    func getCreative(height, width int) *creative.Creative {
        heightMatches := heightIndex[height]
        widthMatches := widthIndex[width]
        for _, heightMatch := range heightMatches {
            for _, widthMatch := range widthMatches {
                if heightMatch == widthMatch {
                    return adMap[heightMatch]
                }
            }
        }
        return nil
    }

    func handleCreativeCall(w http.ResponseWriter, r *http.Request) {
        log.Println("Begin serve call")
        defer func() { log.Println("End serve call") }()
        height, _ := strconv.Atoi(r.URL.Query().Get("height"))
        width, _ := strconv.Atoi(r.URL.Query().Get("width"))
        ad := getCreative(height, width)
        if ad == nil {
            log.Printf("ERROR - Creative with matching width [%d] and height [%d] not found\n", width, height)
            http.Error(w, "Not Found", http.StatusNotFound)
            return
        }

        if _, exists := adStats[int(ad.Id)]; exists == false {
            adStats[int(ad.Id)] = creative.NewCreativeStat()
        }

        fullPath := filepath.Join(staticFilePath, "images", ad.Path)
        _, err := os.Stat(fullPath)
        if err != nil {
            log.Fatal(err)
        }

        http.ServeFile(w, r, fullPath)

        stat := adStats[int(ad.Id)]
        recordImpression(stat, ad)
    }

    func main() {
        log.Println("---starting adserver---")
        http.HandleFunc("/ad", handleCreativeCall)
        appNexusCreative := creative.NewCreative("appnexus-logo.png", 640, 480)
        registerCreative(appNexusCreative)
        http.ListenAndServe(":8081", nil)
        log.Println("---stopping adserver---")
    }

I've made all of this code available in an ["adserver" repo on GitHub](https://github.com/jeffknupp/adserver). Feel free to clone
and build it if you were having problems with the examples above.

## Summing Up

While this is a Python blog first and foremost, I would be remiss if I didn't
describe other technologies I'm interested in and toying with. I hope that, if
you made it to the end, here, you don't consider it having been a waste of your
time. Part of being a professional programmer is growing and stretching your
skills, as it's easy to just slide by on your skills in one technology. We
become better developers, however, by continuing to explore, tinker, and hack.
And, of course, it's important to share your findings with others, if only to
get them thinking.
